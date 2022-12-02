# Бот по подготовке к экзамену по матанализу. 

Этот бот создан для того, чтобы успешно подготавливать определения к любым предметам (в данной реализации этот предмет - матан) и определить все свои слабые места.

# Как пользовататься

Чтобы начать общение с ботом нужно написать коммадну /start. Тогда бот поприветствует вас и расскажет о себе, после чего у вас будет возможность выбрать: 
1) Новое определение. Тогда бот выдасть вам рандомное определение из общего пула, и уйдет в режим ожидания. Ваша задача написать на листочке или просто проговорить
вслух это определение. Когда вы будете готовы, нажмите кнопку "Показать правильный ответ" и, неожиданно, вы увидете правильное определение. Теперь осталось только 
сравнить то, что вы написали сами и что выдал бот, и с помощью кнопок ("да", "нет") сообщить спавились ли вы или нет. Бот запомнит это и запишет в статистику. После этого вы можете
закончить разговор с ботом или начать с первого выбора.
2) Статистика. В этом случае бот Отправит в чат статистику правильных ответов пользователя разделенную по билетам, после этого бот сразу вернется к предыдущему пункту.

# Преимущества

1) Бот написан с помощью ассинхронного модуля aiogram, что позволяет ему работать быстрее и без проблем работать с несколькоми пользователями одновременно
2) Используется база данных на основе sqlite3, которая позволяет хранить свою статистику для каждого пользователя и не терять ее при прекращении работы бота
3) Статистика делится по билетам, что позволяет более точно понять в каком месте учебной программы слабое место (определения беруться из электронных заметок Николая Анатольевича Гусева, поэтому чтобы найти интересующие определения можоно просто зайти на этот сайт и перейти в нужный раздел
4) В бот очень легко добавить новые определения (или совсем поменять предмет). Нужно всего лишь закинуть в папку defenitions/ фотографию нового определения, и в файл defentitions.txt добавить текстовое определение, путь к скиншоту, билет, по общему правилу (Однако перед этим нужно удалить датабазу, поэтому будте аккуратны). После чего перезапустить бота и новые определения уже будут в общем пуле.

# Как запустить
с помощью комманд в терминале получим доступ к репрозиторию:

```
git clone https://github.com/rudanil4/Preparation_for_calculus.git
cd Preparation_for_calculus
git checkout dev
pip install -r requirements.txt
```
После этого необходимо создать токен и добавить его в репрозиторий с именем token.txt

После чего достаточно выполнить 

```
python3 main.py
```

