from .voicebox import Voicebox
from espeakng import ESpeakNG
from io import BytesIO
import wave
import audioop


class ESpeakVoicebox(Voicebox):

    def __init__(self):
        # ♥♥
        self._espeak = ESpeakNG(voice='mb-de3-en', speed=100, volume=50, word_gap=1, pitch=50)  # volume -> -a amplitude
        #  Preset voice options (since they dependent on the system / espeak installation)
        self._preset_voices = {
            'alfred_like': {
                'voice': 'mb-en1',
                'speed': 135,
                'amplitude': 50,
                'gap': 1,
                'pitch': 50
            },
            'jarvis_like': {
                'voice': 'mb-en1',
                'speed': 135,
                'amplitude': 50,
                'gap': 1,
                'pitch': 70
            },
            'anna': {
                'voice': 'mb-de3-en',
                'speed': 100,
                'amplitude': 50,
                'gap': 1,
                'pitch': 50
            },
            'soft_robotic_female': {
                'voice': 'mb-sw2-en',
                'speed': 135,
                'amplitude': 50,
                'gap': 1,
                'pitch': 50
            },
            'robotic_female': {
                'voice': 'mb-us1',
                'speed': 100,
                'amplitude': 50,
                'gap': 1,
                'pitch': 50
            }
        }

    def reconfigure(self, voice_name):
        """
        :param voice_name: Preset voice name.
        :return: <str> Information what changed (if anything).
        """
        if voice_name not in list(self._preset_voices.keys()):
            return 'Invalid voice name. Available: {}'.format(', '.join(list(self._preset_voices.keys())))
        else:
            voice_configuration = self._preset_voices[voice_name]
            changed = []
            if self._espeak.voice != voice_configuration['voice']:
                self._espeak.voice = voice_configuration['voice']
                changed.append('Pronunciation to {}'.format(voice_configuration['voice']))
            if self._espeak.speed != voice_configuration['speed']:
                faster = voice_configuration['speed'] > self._espeak.speed
                self._espeak.speed = voice_configuration['speed']
                changed.append('Speed {} to {} WPM'.format('up' if faster else 'down', voice_configuration['speed']))
            if self._espeak.volume != voice_configuration['amplitude']:
                louder = voice_configuration['amplitude'] > self._espeak.volume
                self._espeak.volume = voice_configuration['amplitude']
                changed.append('Volume {} to {}%'.format('up' if louder else 'down', voice_configuration['amplitude']))
            if self._espeak.word_gap != voice_configuration['gap']:
                self._espeak.word_gap = voice_configuration['gap']
                changed.append('Word gap to {}x'.format(voice_configuration['gap']))
            if self._espeak.pitch != voice_configuration['pitch']:
                higher = voice_configuration['pitch'] > self._espeak.pitch
                self._espeak.pitch = voice_configuration['pitch']
                changed.append('Pitch {} to {}%'.format('up' if higher else 'down', voice_configuration['pitch']))
            if changed:
                return 'Voice changed to preset {} ({})'.format(voice_name, ', '.join(changed))
            else:
                return 'Nothing changed, voice was already in given configuration'

    def utter(self, phrase):
        """
        :param phrase: String containing the words to speak.
        :return: File-like object containing 48kHz stereo PCM data
        """
        # Create PCM as-bytes
        synthesized_wav_bytes = self._espeak.synth_wav(phrase)
        # Upsample bytes to the frequency discord normally uses (48'000 Hz)
        with wave.open(BytesIO(synthesized_wav_bytes)) as wh:
            resampled_bytes, convert_state = audioop.ratecv(synthesized_wav_bytes, wh.getsampwidth(), wh.getnchannels(),
                                                            wh.getframerate(), 48000,
                                                            None)
            resampled_stereo_bytes = audioop.tostereo(resampled_bytes, wh.getsampwidth(), 1, 1)
            return BytesIO(resampled_stereo_bytes)
