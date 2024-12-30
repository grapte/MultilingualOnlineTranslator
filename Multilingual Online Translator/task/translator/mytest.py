import subprocess
import unittest
from pathlib import Path


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # if files ending in .txt exist in the current directory, remove them
        if files := list(Path('.').glob('*.txt')):
            for obj in files:
                obj.unlink()

    def run_command(self, *args):
        command = ['python', 'translator.py'] + list(args)
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def test_example1(self):
        result = self.run_command('english', 'korean', 'hello')
        self.assertIn("Sorry, the program doesn't support korean", result.stdout)
        self.assertEqual(result.returncode, 0,f"Script failed with error:\n{result.stderr}")

    def test_example2(self):
        word = 'hello'
        result = self.run_command('english', 'all', word)
        with open(f'{word}.txt') as file:
            text = file.read()
        for w in [word, 'hola', 'hallo']:
            self.assertIn(w, text)
        self.assertEqual(result.returncode, 0, f"Script failed with error:\n{result.stderr}")

    def test_example3(self):
        result = self.run_command('english', 'all', 'brrrrrrrrrrr')
        self.assertIn('Sorry, unable to find brrrrrrrrrrr', result.stdout)
        self.assertEqual(result.returncode, 0, f"Script failed with error:\n{result.stderr}")

if __name__ == '__main__':
    unittest.main()
