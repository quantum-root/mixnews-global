# MixNews Global 📰🚀

MixNews Global is a modern, cross-platform news aggregator application that fetches real-time world and national news from various prestigious sources, parsing the data smoothly into a clean and intuitive user interface. 

Built with **Python**, powered by the **Flet framework** (Flutter-backed UI), and driven by advanced **Web Scraping** techniques.

---

## 💡 Evolution of the Project (Where it started)

This project is the highly advanced, refactored, and scalable **v5 version** of my initial software. 

* 🏛️ **The Origin:** The very first, basic version of this application was created as a school project under the name **News Explorer**. You can check out the legacy repository here: [👉 Legacy News Explorer Repo](https://github.com/quantum-root/news-explorer)
* 🚀 **The Evolution:** In this new `mixnews-global` repository, the entire project has been rebuilt from scratch. I migrated the codebase to an asynchronous-friendly modular architecture, separated the news sources into independent scaper components, and completely overhauled the UI/UX using Flet.

---

## ✨ Features

* **Multi-Source Scraping:** Dynamically fetches and parses data from global and local agencies like BBC, Independent, NTV, and Karar.
* **Modular Architecture:** Each news source has its own independent scraper module under the `sources/` package, making it incredibly easy to scale and add new platforms.
* **Modern UI/UX:** Responsive, clean, and visually appealing interface built with Flet.
* **Zero Configuration:** No expensive API keys required. It uses pure pythonic web scraping (`BeautifulSoup4` & `requests`) under the hood.

---

## 📂 Project Structure

```text
mixnews-global/
│
├── main.py                 # Application entry point & UI Router
├── requirements.txt        # Production dependencies
├── LICENSE                 # MIT License open-source protection
│
└── sources/                # Dedicated scraper package
    ├── __init__.py         # Package initializer
    ├── news_bbc_en.py
    ├── news_independent_en.py
    ├── news_karar_tr.py
    └── news_ntv_tr.py
```

---

## 🛠️ Installation & Setup

To run this project locally, follow these simple steps:

1. Clone the repository using the git clone command with your repository URL.
2. Navigate into the project folder using the change directory command.
3. Install the required production dependencies listed in the requirements file.
4. Run the application entry point file to start the interface.

```bash
git clone [https://github.com/quantum-root/mixnews-global.git](https://github.com/quantum-root/mixnews-global.git)
cd mixnews-global
pip install -r requirements.txt
python main.py
```

---

## 📝 License

Distributed under the MIT License. See LICENSE for more information.
