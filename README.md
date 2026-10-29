# Эмулятор оболочки ОС (Вариант 24)

## 1. Общее описание

Эмулятор командной строки UNIX-подобной ОС на Python.
Работает с виртуальной файловой системой (VFS) из JSON
и поддерживает интерактивный режим (REPL) и пакетное
выполнение скриптов.

## 2. Описание функций и настроек

- `--vfs`: путь к JSON-файлу VFS.
- `--script`: путь к стартовому скрипту.
- Команды: `ls`, `cd` (заглушки), `exit`.
- Раскрытие переменных окружения `$VAR` и `${VAR}`.

## 3. Команды для сборки и запуска тестов

```bash
chmod +x run.sh tests/run_tests.sh
./run.sh
./run.sh --vfs tests/test_vfs_complex.json \
    --script tests/test_all.sh
./tests/run_tests.sh

## 4. Примеры использования

```bash
$ ./run.sh
[default_vfs /]$ echo $HOME
/home/user
[default_vfs /]$ exit
