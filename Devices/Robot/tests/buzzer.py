#
# Buzzer
#
# Version 24_08_03_02
#
from machine import Pin, PWM
from time import sleep
import uasyncio as asyncio

class Buzzer:
    DUTY_CYCLE: int = 5000
    FOREVER: int = -1
    
    # Octave 4, starting at Middle C
    note_freqs = {"C": 262, "C#": 277, 
                  "D": 294, "D#": 311, 
                  "E": 330, 
                  "F": 349, "F#": 370, 
                  "G": 392, "G#": 415, 
                  "A": 440, "A#": 466, 
                  "B": 494,
                  "R": 0, "X": 0} # Rest
    
    def __init__(self, pin: int=10) -> None:
        self.buzzer = PWM(Pin(pin, Pin.OUT))
        self.playing = False
        
    def beep(self, repeat: int=1, freq: int=440, duration: float=0.1, delay: float=0.1)-> None:
        """Make a single beep at a given frequency and duration.
        
        Args:
            repeat (int, optional): number of times to repeat. Defaults to 1.
            freq (int, optional): Frequency of the beep (Hz). Defaults to 440.
            duration (float, optional): Duration of the beep (sec). Defaults to 0.1.
            delay (float, optional): Delay after beep (sec). Defaults to 0.1.
        """
        for i in range(repeat):
            self._play_note(freq, duration)
            sleep(delay)
        
    def begin_sound(self)-> None:
        """Make a startup sound.
        """
        self.play( [262, 392, 0], [0.2, 0.2, 0.4], delay=0.0)
        
    def end_sound(self)-> None:
        """Make a shutdown sound.
        """
        self.play( [392, 262, 0], [0.2, 0.2, 0.4], delay=0.0)
        
    def play(self, notes: list, beats: list, delay: float=0.01, repeat: int=1)-> None:
        """Play a sequence of notes.    
        Args:
            notes (list): list of note names or frequencies (Hz) (int) or 'R' or 'X' for 'rest'
            beats (list): list of note durations (sec) (float)
            delay (float, optional): delay after each note (sec). Defaults to 0.01.
            repeat (int, optional): number of times to repeat. Defaults to 1. 
        """
        for _ in range(repeat):
            for note, beat in zip(notes, beats):
                if Buzzer.note_freqs.get(note):
                    self._play_note(Buzzer.note_freqs[note], beat, delay)
                elif type(note) == int:
                    self._play_note(note, beat, delay)
                else:
                    sleep(beat + delay)
                
    async def play_async(self, notes: list, beats: list, delay: float=0.01, repeat: int=1)-> None:
        """Play a sequence of notes.    
        Args:
            notes (list): list of note names or frequencies (Hz) (int) or 'R' or 'X' for 'rest'
            beats (list): list of note durations (sec) (float)
            delay (float, optional): delay after each note (sec). Defaults to 0.01.
            repeat (int, optional): number of times to repeat
        """
        self.playing = True
        while self.playing and repeat != 0:
            for note, beat in zip(notes, beats):
                if Buzzer.note_freqs.get(note):
                    await self._play_note_async(Buzzer.note_freqs[note], beat, delay)
                elif type(note) == int:
                    await self._play_note_async(note, beat, delay)
                else:
                    asyncio.sleep(beat + delay)
            repeat = max(repeat-1, -1)
        
    def _play_note(self, note: int, duration: float, delay: float=0.01)-> None:
        if note == 0:
            sleep(duration + delay)
            return
        self.buzzer.freq(note)
        self.buzzer.duty_u16(Buzzer.DUTY_CYCLE)
        sleep(duration)
        self.buzzer.duty_u16(0)
        sleep(delay)
        
    async def _play_note_async(self, note: int, duration: float, delay: float=0.01)-> None:
        if note == 0:
            await asyncio.sleep(duration + delay)
            return
        self.buzzer.freq(note)
        self.buzzer.duty_u16(Buzzer.DUTY_CYCLE)
        await asyncio.sleep(duration)
        self.buzzer.duty_u16(0)
        await asyncio.sleep(delay)
        
    def stop_async(self)-> None:
        self.playing = False
                
                
            
# Test 
async def wait(buzzer):
    print('starting wait')
    await asyncio.sleep(2)
    buzzer.stop_async()

async def play_song(buzzer):
    print('starting play_song')
    notes = [262, 0, 294, 330, 349, 392, 440, 494, 523]
    beats = [0.05 for note in notes]
    print(f'Playing a song using frequency notation: {notes}')
    await buzzer.play_async(notes, beats, repeat=Buzzer.FOREVER)
    print('ending play_song')


if __name__ == '__main__':
    buzzer = Buzzer(pin=22)
    
    try:
        print('Trying interrupted looped song')
        asyncio.run( asyncio.gather(wait(buzzer), play_song(buzzer)))
        sleep(1)
        
        print('Async buzzer')
        asyncio.run(buzzer._play_note_async(200, 0.5))
        sleep(1)
    
        notes = [262, 0, 294, 330, 349, 392, 440, 494, 523]
        beats = [0.15 for note in notes]
        print(f'Async playing a song using frequency notation: {notes}')
        asyncio.run(buzzer.play_async(notes, beats))
        sleep(1)
    
        # Single beep
        print('Single beep')
        buzzer.beep()
        sleep(1)
        
        # Single beep
        print('Multiple beep')
        buzzer.beep(repeat=2, freq=500)
        sleep(1)
        
        # Print beginning and ending sounds
        print('Begin and  end sounds')
        buzzer.begin_sound()
        buzzer.end_sound()
        sleep(1)

        # Play a song using notes notation
        notes = ["C", "R", "D", "E", "F", "G", "X", "A", "B", "C" ]
        beats = [0.25 for note in notes]
        print(f'Playing a song using notes notation: {notes}')
        buzzer.play(notes, beats)
        sleep(1)
        
        # Play a song using frequency notation
        notes = [262, 0, 294, 330, 349, 392, 440, 494, 523]
        beats = [0.1 for note in notes]
        print(f'Playing a song using frequency notation: {notes}')
        buzzer.play(notes, beats, repeat=2)
    
    except KeyboardInterrupt:
        print('Program ended.')

