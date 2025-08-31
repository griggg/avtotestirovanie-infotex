# avtotestirovanie-infotex

## Инструкции по запуску
1) Склонируйте репозиторий
2) Установите зависимости requirements.txt (httpx)
3) Запустите main.py с необходимыми аргументами

<img width="1645" height="419" alt="image" src="https://github.com/user-attachments/assets/c507fc2f-7a42-4623-82be-8c16c652c1ad" />

## Примеры вывода

```bash
python3 main.py -H https://ya.ru,https://google.com -C 5
```
<img width="1687" height="740" alt="image" src="https://github.com/user-attachments/assets/3133f645-0afa-4ef7-82d6-cae25c925700" />

```bash
python3 main.py -H invalid_url,http://valid.com -C 1 
```
<img width="1555" height="465" alt="image" src="https://github.com/user-attachments/assets/48ed663a-944a-46a8-bb81-c3e8421e879d" />

```bash
echo "sadfafas
https://ya.ru" > hosts.txt

python main.py -F hosts.txt -C 5 -O results.txt

cat results.txt
```

<img width="1890" height="591" alt="image" src="https://github.com/user-attachments/assets/deecf93a-f361-4f18-b1e0-0107dddd64b5" />

