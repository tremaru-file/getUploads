import getUploads as gu
import RPi.GPIO as GPIO
from time import sleep
import sys

# установки
filename = "vids.txt"
channelname = str(sys.argv[1])

# вывод сервопривода
servopin = 12
# ШИМ верхнего и нижнего положения
servodown = 5   # %
servoup = 10    # %

# устанавливаем выводы
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT)

# создаём объект сервопривода
servo = GPIO.PWM(servopin, 50)

# узнаём количество загруженных видео на канале
vidsnumber = gu.getUploadsNumber(channelname)

# функция перезаписи файла
def rewrite(name):
    f = open(name, 'w')
    f.write(str(vidsnumber))
    f.close()

# основной код
try:

    # пробуем открыт файл
    myfile = open(filename, 'r')

# если файл не найден
except FileNotFoundError:

    # записываем данные в файл
    rewrite(filename)
    # cерво вниз
    servo.start(servodown)
    servo.stop()
    GPIO.cleanup()
    # выходим из сценария
    exit()

# если файл найден
else:

    try:

        # пробуем преобразовать данные в файле
        storednumber = int(myfile.read()) 

    # если в файле не цифры
    # закрываем, перезаписываем файл
    except ValueError:

        myfile.close()
        rewrite(filename)
        exit()

    # если количество загрузок не изменилось
    # со вермени последнего запроса
    # опускаем серво
    if storednumber == vidsnumber:

        myfile.close()
        servo.start(servodown)

    # если количество загрузок меньше
    # чем в прошлый раз (другой канал или видео были удалены)
    # перезаписываем файл
    elif vidsnumber < storednumber:

        myfile.close()
        rewrite(filename)

    # если ничего из вышеперечисленного,
    # значит новое видео!
    # поднимаем серво, перезаписываем файл
    else:

        myfile.close()
        rewrite(filename)
        servo.start(servoup)
    
    # прибераемся за собой
    sleep(.5)
    servo.stop()
    GPIO.cleanup()
