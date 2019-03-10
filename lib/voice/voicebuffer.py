import asyncio
import time


class StateError(Exception):
    def __init__(self, message):
        super().__init__(message)


class VoiceBuffer:
    def __init__(self, anna, voicebox, priorities=None):
        self._anna = anna
        self._voicebox = voicebox
        self._is_active = False
        self._currently_active_in = None  # String, server name
        self._currently_activated_by = None  # String, username#discriminator
        self._voice_client = None
        self._is_speaking = False
        # Init message queue and make shallow copy of priorities argument
        if priorities is None:
            priorities = []
        self._priorities = list(priorities)  # ['LOWEST_PRIORITY_IDENTIFIER', ..., 'HIGHEST_PRIORITY_IDENTIFIER']
        self._queued_messages = []  # [[phrase, priority_integer, time_added_int], ...]

    def add_to_queue(self, phrase, priority=None, lowest_priority=False, highest_priority=False):
        """
        Intended to be used by background processes directly (i.e. no user involved)

        :param phrase: A string to add in queued messages. If no priority is indicated it will be set to 0
        :param priority: A string to lookup from self._priorities, and use its index as the value to pass as priority.
        :param lowest_priority: A flag to set True if message should have lowest priority (overrides arg "priority")
        :param highest_priority: A flag to set True if message should have highest priority (overrides all other args)
        :return: None
        """
        interpreted_priority = 0
        if highest_priority:
            interpreted_priority = max(map(lambda m: m[1], self._queued_messages))
        elif lowest_priority:
            pass  # The default, presumably no "< 0" priorities (unless programmatically set, but those are exceptions)
        elif priority is not None and priority in self._priorities:
            interpreted_priority = self._priorities.index(priority)
        self._queued_messages.append([phrase, interpreted_priority, int(time.time())])

    async def activate(self, requester, server):
        """
        :param requester: discord <User> (or superclass Member)
        :param server: discord <Guild>
        """
        if self.is_voice_initialized():
            return
        # Activating voice client is asynchronous, set flags first preventing race-conditions
        self._is_active = True
        self._currently_activated_by = '{}#{}'.format(requester.name, requester.discriminator)
        self._currently_active_in = server.name
        voice_client = await self._anna.join_voice_channel(requester.voice.voice_channel)
        self._voice_client = voice_client

    def deactivate(self):
        """
        :return: Either None (if noop) or only-assert-able concurrent.futures.Future
        """
        if not self.is_voice_initialized():
            return
        future = asyncio.run_coroutine_threadsafe(self._voice_client.disconnect(), self._voice_client.loop)
        self._voice_client = None
        self._currently_activated_by = None
        self._currently_active_in = None
        self._is_active = None
        return future

    def is_voice_initialized(self):
        return self._is_active and self._voice_client

    async def speak(self, phrase, cb_after=None):
        """
        :param phrase: String of words to speak
        :param cb_after: Optional callback to run after finished speaking
        """
        if not self.is_voice_initialized():
            raise StateError("Voice capabilities must first be active, use method <VoiceBuffer>.is_voice_initialized()")
        if self._is_speaking:
            self.add_to_queue(phrase, lowest_priority=True)
            return
        else:
            self._is_speaking = True

            def finished_speaking():
                self._is_speaking = False
                if cb_after is not None:
                    cb_after()

            # Generate PCM stream and pass it to voice client
            readable_wave = self._voicebox.utter(phrase)
            self._voice_client.encoder_options(sample_rate=48000, channels=2)
            player = self._voice_client.create_stream_player(readable_wave, after=finished_speaking)
            player.start()
