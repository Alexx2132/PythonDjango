from django.core.exceptions import PermissionDenied, BadRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseForbidden, HttpResponseServerError, HttpResponseBadRequest
from django.urls import register_converter
Students = [
    {'id':1, 'FI': 'Буренок Дмитрий', 'date':'14.01.2005', 'pol':'boy'},
    {'id':2, 'FI': 'Горбанёв Кирилл', 'date':'25.01.2006', 'pol':'boy'},
    {'id':3, 'FI': 'Капшукова Дарья', 'date':'27.06.2004', 'pol':'girl'},
    {'id':4, 'FI': 'Кашаева Раяна', 'date':'27.06.2004', 'pol':'girl'},
    {'id':5, 'FI': 'Климин Тимур', 'date':'17.05.2004', 'pol':'boy'},
    {'id':6, 'FI': 'Косенков Глеб', 'date':'9.06.2004', 'pol':'boy'},
    {'id':7, 'FI': 'Костин Максим', 'date':'3.04.2001', 'pol':'boy'},
    {'id':8, 'FI': 'Кузенков Богдан', 'date':'01.01.2003', 'pol':'boy'},
    {'id':9, 'FI': 'Миколадзе Антон', 'date':'14.09.2004', 'pol':'boy'},
    {'id':10, 'FI': 'Мишин Александр', 'date':'21.08.2004', 'pol':'boy'},
    {'id':11, 'FI': 'Мишин Алексей', 'date':'21.08.2004', 'pol':'boy'},
    {'id':12, 'FI': 'Пешеходько Арсений', 'date':'01.01.2004', 'pol':'boy'},
    {'id':13, 'FI': 'Сентюрина Екатерина', 'date':'08.11.2002', 'pol':'girl'},
]
events = {2000: '<li>На экраны вышел «Брат 2»</li><li>Затонула подлодка «Курск»</li>\
                    <li>В России созданы федеральные округа и институт полномочных представителей Президента РФ в них</li><li>Победа В.В. Путина на выборах президента России</li>',
              2001: '<li>Нападение боевиков на Гудермес</li><li>Cтанция «Мир» была затоплена в Тихом океане</li><li>Старт корабля Союз ТМ-32</li><li>ВИЗИТ ПАПЫ РИМСКОГО В КАЗАХСТАН </li>',
              2002: '<li>Бразилия - чемпион мира по футболу. В пятый раз в истории.</li><li> Россия выигрывает командный чемпионат мира по теннису, впервые в истории.</li><li>КНДР признала себя ядерной державой</li><li>Катастрофа танкера "Престиж"</li>',
              2003: '<li>Референдум в Чечне</li><li>Новый этап экономических реформ</li><li>Реформирование силовых структур</li><li>Выход КНДР из Договора о Нераспространении ядерного оружия/</li>',
              2004: '<li>Начала работу социальная сеть Facebook</li><li>Главой Российской Федерации повторно избран Владимир Путин</li><li>Президент РФ подписал Закон о льготных выплатах</li><li>Террористический акт в средней школе №1 в городе Беслане</li>',
              2005: '<li>Казань в 2005 году праздновала своё 1000-летие.</li><li>Сформирована Общественная палата РФ</li><li>Президент РФ сформулировал национальные приоритеты в развитии страны: современное здравоохранение, качественное образование, доступное жилье и эффективное сельское хозяйство</li><li>Создан сервис YouTube</li>',
              2006: '<li>Создание социальной сети ВКонтакте</li><li>Начала работу социальная сеть «Одноклассники»</li><li>В России утверждено Почётное звание «Город воинской славы»</li><li>Открылись XX зимние Олимпийские игры в Турине (Италия)</li>',
              2007: '<li>Компания Apple представила первое поколение смартфона iPhone</li><li>Microsoft начала официальные продажи Windows Vista в России</li><li>Рамзан Кадыров стал главой Чеченской Республики</li><li>Российские батискафы "Мир" впервые в истории опустились на дно океана в точке северного полюса.</li>',
              2008: '<li>Вышла в свет первая версия платформы Android</li><li>10 сентября запущен Большой адронный коллайдер. Вопреки прогнозам пессимистов планета уцелела.</li><li>Дмитрий Медведев стал президентом РФ</li><li>Образован новый субъект РФ - Иркутская область</li>',
              2009: '<li>Американское космическое агентство NАSА запустило в космос мощный телескоп «Kepler»</li><li>ЮНЕСКО запустило Всемирную цифровую библиотеку</li><li>В России вступил в силу закон, по которому казино и другие игорные заведения могут легально существовать только в специально созданных игровых зонах</li><li>Начались розничные продажи новой операционной системы Windows 7</li>',
              2010: '<li>Начало работы первого кириллического домена</li><li>Начало продаж iPad</li><li>Официальное окончание войны в Ираке</li><li>Вступил в силу Таможенный союз России, Белоруссии и Казахстана</li>',
              2011: '<li>Милицию переименовали в полицию</li><li>Отмена перехода на зимнее время</li><li>Ким Чен Ын официально объявлен вождем КНДР</li><li>На планете стало 7 миллиардов человек</li>',
              2012: '<li>Путин снова стал президентом РФ</li><li>В России, Белоруссии и Казахстане создано Единое экономическое пространство</li><li>Открытие моста на остров Русский</li><li>К МКС пристыковался первый частный корабль: начинается эпоха Илона Маска</li>',
              2013: '<li>Начало действия антитабачного закона</li><li>Запущен официальный онлайн-магазин Apple в России</li><li>Эдвард Сноуден — разоблачитель года</li><li>В начале 2013 года на жителей Челябинска обрушился метеорит</li>',
              2014: '<li>Воссоединение Крыма С Россией</li><li>Провозглашение Донецкой и Луганской народных республик</li><li>Олимпиада в Сочи</li><li>Россия перешла на постоянное зимнее время</li>',
              2015: '<li>Семидесятилетие Победы в Великой Отечественной войне</li><li>Выпуск первых карт «Мир»</li><li>Вступил в силу договор о создании ЕАЭС</li><li>Заключены Минские соглашения</li>',
              2016: '<li>С космодрома «Восточный» успешно запустили первую ракету</li><li>Закон об ограничении деятельности коллекторов</li><li>Образование Росгвардии</li><li>Дональд Трамп избран президентом США</li>',
              2017: '<li>Кубок конфедераций в России</li><li>Закон о признании СМИ иноагентами</li><li>Путин приказал выводить российские войска из Сирии</li><li>Первый в мире электрический грузовик</li>',
              2018: '<li>Открытие Крымского моста</li><li>Пожар в «Зимней вишне»</li><li>Повышение пенсионного возраста</li><li>Новая ядерная доктрина США</li>',
              2019: '<li>Закон о «суверенном интернете»</li><li>США снова вышли из ЮНЕСКО и впервые — из Договора о ликвидации ракет средней и меньшей дальности</li><li>Пожар в соборе Парижской Богоматери</li><li>Отставка Нурсултана Назарбаева</li>',
              2020: '<li>Коронавирус в России</li><li>Роскомнадзор разблокировал Telegram </li><li>Русский газ пошел в Турцию</li><li>Президент Белоруссии Александр Лукашенко был переизбран на шестой срок с неоднозначным процентным превосходством. </li>',
              2021: '<li>Вступил в силу закон о цифровых финансовых активах</li><li>«Магнит» купил сеть «Дикси»</li><li>Цена на газ в Европе впервые в истории превысила $1000 </li><li>Смена бренда и акционеров VK</li>',
              2022: '<li>XXIV зимние Олимпийские игры в Китае</li><li>Начало спецоперации на Украине </li><li>Илон Маск купил Twitter</li><li>Население Земли 15 ноября официально достигло восьми миллиардов человек</li>',
              2023: '<li>Укрепление влияния Китая в мире</li><li>Избрание нового генерального секретаря ООН</li><li>Реформа системы образования в России</li><li>Взятие Артёмовска российскими войсками</li>'}

menu = [{'title':'Главная', 'url_n':'home'}, {'title':'О программе', 'url_n':'about'}, {'title':'Список группы ИСТ-201', 'url_n':'mpage'}]

data = {'title' : 'Главная страница',
            'menu':menu,
        'students':Students,
            }

def index(request):

    #return HttpResponse("страница приложения students")
    return render(request, 'student/index.html', context=data)

def about(request):
    return render(request, 'student/about.html', context=data)

def students_mainpage(request):

    #if(request.GET):
        #string = str()
        #for key in request.GET:
            #string += key + ": " + request.GET[key] + ", "
        #return HttpResponse(f"<h2>Вы ввели GET-запрос</h2> <p>Содержание: {string[:-2]}</p>")
    #return HttpResponse("<h1>Главная страница students</h1> <p>Для отображения информации о конкретном студенте введите индекс в URL. Также можно вывести GET-запрос</p>")
    return render(request, 'student/students.html', context=data)


def students_id(request, studid):
    # if 0 < studid < 14:
    #     return HttpResponse(f"<h1>Студент группы ИСТ-201</h1><p>{Students[studid - 1]}</p>")
    # elif studid == 15:
    #     return redirect('home')
    # else:
    #     return HttpResponse(f'<h1>Студент не найден</h1>')
    return render(request, 'student/one_student.html', context=Students[studid - 1])

def year(reguest, year_id):
    if 2000 <= int(year_id) <= 2023:
        return HttpResponse(f"<h1>События {year_id} года</h1> <ul>{events[int(year_id)]}</ul>")
    elif int(year_id) == 2025:
        return redirect('home', permanent=True)
    else:
        return HttpResponse(f"<h1>{year_id} год отсутствует в списке</h1>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>404 Страница не найдена</h1>')

def h_403(request, exception):
    return HttpResponseForbidden('<h1>403 Доступ запрещён</h1>')

def h_500(request):
    return HttpResponseServerError('<h1>500 Ошибка сервера</h1>')

def h_400(request, exception):
    return HttpResponseBadRequest('<h1>400 Плохой запрос</h1>')

def e_400(request):
    raise BadRequest

def e_500(request):
    return errrrrrr

def e_403(request):
    raise PermissionDenied()