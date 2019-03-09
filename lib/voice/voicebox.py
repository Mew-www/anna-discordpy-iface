from abc import ABC, abstractmethod


class Voicebox(ABC):

    @abstractmethod
    def reconfigure(self, new_configuration):
        """To re-configure voice."""
        pass

    @abstractmethod
    def utter(self, phrase):
        """To produce sound (essentially TTS). 48'000Hz stereo PCM-data required by Discord."""
        pass
