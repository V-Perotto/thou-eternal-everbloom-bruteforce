from pyautogui import locateOnScreen, click, write, press, center
from loguru import logger
from time import sleep
from pathlib import Path
from itertools import product
from string import ascii_lowercase
from traceback import format_exc

## consts
GAME_NAME: str = "Thou Eternal Everbloom (DEBUG)"
ATTEMPTS: int = 0
FOUND: bool = False
PASSWORD: str = ''
IMAGES_PATH: Path = Path('images')
BACKPACK_IMG: str = 'backpack'
BOOK_IMG: str = 'book'
BOOK_EXAMINE_IMG: str = 'book_examine'
ENTER_PASSWORD_IMG: str = 'enter_password'
INCORRECT_IMG: str = 'incorrect'
WHATISTHEPASSWORD_IMG: str = 'whatisthepassword'
FILE_EXTENSION: str = '.png'
ATTEMPTS_FILE: Path = Path("attempts.txt")

## base functions
def setPath(value) -> str:
    return str(IMAGES_PATH / f"{value}{FILE_EXTENSION}")

def savePassword(value) -> bool:
    try:    
        with open("password.txt", "w", encoding="utf-8") as f:
            f.write(value)
        return True
    except Exception as e:
        logger.error("savePassword:", e)

def getNextWord(word):
    word_list = list(word)
    
    for i in range(len(word_list) - 1, -1, -1):
        if word_list[i] != 'z':
            word_list[i] = ascii_lowercase[ascii_lowercase.index(word_list[i]) + 1]
            return "".join(word_list)
        else:
            word_list[i] = 'a'        
    return 'a' + "".join(word_list)

def generateSequence():
    start_word = ''

    if ATTEMPTS_FILE.exists() and ATTEMPTS_FILE.stat().st_size > 0:
        with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            start_word = lines[-1].strip()
    else:
        start_word = 'aaaa'

    current_word = start_word
    
    generated_words = []

    while len(current_word) <= 12:
        yield current_word
        
        generated_words.append(current_word)
        
        current_word = getNextWord(current_word)
        
    with open(ATTEMPTS_FILE, "a", encoding="utf-8") as f:
        for word in generated_words:
            f.write(word + "\n")

def getAndSaveAttempt(new_attempt):
    if ATTEMPTS_FILE.exists():
        attempts = set(ATTEMPTS_FILE.read_text(encoding="utf-8").splitlines())
    else:
        attempts = set()
    if new_attempt in attempts:
        return False
    else:
        attempts.add(new_attempt)
        with open(ATTEMPTS_FILE, "a", encoding="utf-8") as file:
            file.write(new_attempt + "\n")
        return True

## variables
BACKPACK: str = setPath(BACKPACK_IMG)
BOOK: str = setPath(BOOK_IMG)
BOOK_EXAMINE: str = setPath(BOOK_EXAMINE_IMG)
ENTER_PASSWORD: str = setPath(ENTER_PASSWORD_IMG)
INCORRECT: str = setPath(INCORRECT_IMG)
WHATISTHEPASSWORD: str = setPath(WHATISTHEPASSWORD_IMG)

## functions
def locateBackpack():
    try:
        return locateOnScreen(BACKPACK, confidence=0.8)
    except Exception:
        logger.error(f"locateBackpack: {format_exc()}")

def locateBook():
    try:
        return locateOnScreen(BOOK, confidence=0.8)
    except Exception:
        logger.error(f"locateBook: {format_exc()}")

def locateBookExamine() -> bool:
    try:
        return locateOnScreen(BOOK_EXAMINE, confidence=0.8)
    except Exception:
        print(f"locateBookExamine: {format_exc()}")

def locateEnterPassword() -> bool:
    try:
        return locateOnScreen(ENTER_PASSWORD, confidence=0.8)
    except Exception:
        logger.error(f"locateEnterPassword: {format_exc()}")

def locateIncorrect() -> bool:
    try:
        return locateOnScreen(INCORRECT, confidence=0.8)
    except Exception:
        logger.error(f"locateIncorrect: {format_exc()}")

def locateWhatIsThePassword() -> bool:
    try:
        return locateOnScreen(WHATISTHEPASSWORD, confidence=0.8)
    except Exception:
        logger.error(f"locateWhatIsThePassword: {format_exc()}")

## starting program
def startProgram():
    global FOUND, ATTEMPTS
    sleep(5)
    attempt_generator = generateSequence()
    while not FOUND:
        try:
            backpack = locateBackpack()
            if not backpack:
                logger.warning(f"{BACKPACK} not found. Trying again...")
                sleep(1)
                continue
            click(center(backpack))
            sleep(0.2)
            book = locateBook()
            if not book:
                logger.warning(f"{BOOK} not found. Trying again...")
                sleep(1)
                continue
            click(center(book))
            sleep(0.2)
            book_examine = locateBookExamine()
            if not book_examine:            
                logger.warning(f"{BOOK_EXAMINE} not found. Trying again...")
                sleep(1)
                continue
            click(center(book_examine))
            sleep(2)
            whatisthepassword = locateWhatIsThePassword()
            if not whatisthepassword:            
                logger.warning(f"{WHATISTHEPASSWORD} not found. Trying again...")
                sleep(1)
                continue
            click(center(whatisthepassword))
            sleep(0.2)
            enter_password = locateEnterPassword()
            if enter_password:
                click(center(enter_password))            
                current_attempt = next(attempt_generator)
                write(current_attempt, interval=0.1)
                press("enter")
                sleep(2)
                incorrect = locateIncorrect()
                if incorrect:
                    getAndSaveAttempt(current_attempt)
                else:
                    PASSWORD = current_attempt
                    savePassword(PASSWORD)
                    FOUND = True
                    logger.info(f"Founded password: {getAndSaveAttempt}")
        except StopIteration:
            logger.warning("All possible combinations attempted.")
            FOUND = True
            
        except Exception as e:
            logger.error(e)
            sleep(2)

if __name__ == '__main__':
    startProgram()


