# @codereptile_cryptography_bot

## Автор:

Агеев Артём Андреевич

## Описание бота:

Позволяет шифровать сообщения с помощью криптосистемы Эль-Гамаля над группой `G=(Z_p\{0}, *)`.

### Инструкция использования:

#### 1 - Шифрование сообщения: `/encrypt {p} {g} {g^a} {message}`

Шифрует `{message}`, используя `{p}` и `{g}` в качестве настроек для криптосистемы и `{g^ a}` в качестве открытого
ключа.

Внимание: `{p}` должно быть простым числом!

Пример:
```text
/encrypt 1000000901 76124921 274331954 Some text
```


Возможный вывод:

```text
Your encrypted message:
795098598 610348920
338750833 122342864
188644788 170912063
414357401 474766981
334621182 75671140
627117401 273229359
426912698 586443833
611125742 540364801
328890681 109675082
-1
```

#### 2 - Расшифрование сообщения: `/decrypt {p} {a} {encrypted-message}`

Расшифровывает `{encrypted-message}`, используя `{p}` в качестве параметра для криптосистемы и `{a}` в качестве
приватного ключа.

Пример: 
```text
/decrypt 1000000901 274611592
795098598 610348920
338750833 122342864
188644788 170912063
414357401 474766981
334621182 75671140
627117401 273229359
426912698 586443833
611125742 540364801
328890681 109675082
-1
```

Возможный вывод:

```text
Your decrypted message:
Some text
```

## Server:

Собственный сервер на `ubuntu-impish`.

Стоит на другом конце города, доступ: `ssh`, `vnc` (на крайний случай).

Серверу выделил статический IP, доменное имя. Он уже очень давно у меня, использовал
для [самодельного gitlab-сервера](https://gitlab.codereptile.ru) (дабы не было ограничений).

## CD on server-side:

Сделал скрипт, запускающий docker-compose с watch-tower при запуске/перезапуске системы.
