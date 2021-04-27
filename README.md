|HWHelper|
|---|
|Simple bot to help  HackerWars Community on VK|
|========================================================| 
| - Later here will appears installation guide or some facts|
| - Some time after here will be instruction of installation|

- This bot works on python 3.7 and using MySQL 5.6 as database 
- Bot is expecting to host on PythonAnywhere because it's free and have some limits
- In instructions will be appeared all packages that you need to install
    - For now list is: Flask, vk, MySQLdb, requests  
- This project is open-source and after full deploying you can download it and setup in your fraction 
    - So that means you will be able to re-write almost anything that you want
- `settings.py` file is used to configure start of the bot, and it will be change
- Also sometimes you can see some token or something like that. Don't worry, I have already changed it :)
- All modules have description at start. You can always check what this module used to


Here will be short description of modules:

| Module    | Purpose of module                                         |
|-----------|-----------------------------------------------------------|
|`commands` | All commands of bot which starts with prefix (default: / )|
|`forwards` | All handlers with forward messages                        |
|`hw_api`   | Requests about __HackerWars__                             |
|`payloads` | All buttons of bot, maybe including pages                 |
|`settings` | Initial values to start bot                               |
|`start`    | Initial module and main handler of bot                    |
|`vk_api`   | API of [vk.com](https://vk.com)                           |
|`db.db_sql`| Connector to database                                     |
|`db.users` | Users Entity in database                                  |
|`db.squads`| Squads Entity in database                                 |

