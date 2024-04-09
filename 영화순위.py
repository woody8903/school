import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests

# HTML 내용. 실제 사용 시에는 requests.get(url).text로 웹페이지의 HTML을 가져옵니다.
url = "https://www.moviechart.co.kr/rank/boxoffice"

response = requests.get(url)

# BeautifulSoup 객체 생성
soup = BeautifulSoup(response.text, 'html.parser')

# 영화 정보를 추출하는 함수
def extract_movie_data(soup):
    movies = []
    for row in soup.select('.listTable tbody tr'):
        movies.append([
            row.select_one('td.redAc').text.strip(),  # 순위
            row.select_one('td.title a').text.strip(),  # 영화명
            row.select_one('td.date').text.strip(),  # 개봉일
            row.select_one('td.audience').text.strip(),  # 관객수
            row.select_one('td.cumulative').text.strip(),  # 누적관객수
            row.select_one('td.sales').text.strip(),  # 누적매출액
        ])
    return movies

# GUI 애플리케이션 생성
class MovieApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Movie Ranking')
        self.geometry('800x600')
        self.create_widgets()

    def create_widgets(self):
        columns = ('Rank', 'Title', 'Release Date', 'Audience Count', 'Cumulative Audience', 'Cumulative Sales')
        self.treeview = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor='center')
        self.treeview.pack(fill='both', expand=True)
        self.load_movie_data()

    def load_movie_data(self):
        movies = extract_movie_data(soup)
        for movie in movies:
            self.treeview.insert('', 'end', values=movie)

if __name__ == '__main__':
    app = MovieApp()
    app.mainloop()
