#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

from douban.bs4_3_get_top import get_top_movies


class MovieDescription:
    def __init__(self, description_dict):
        for key, value in description_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        return (
            f"Title: {self.电影名}\n"
            f"Rank: {self.电影排名}\n"
            f"Plot: {self.概览}\n"
        )


def get_all_final_movies(list):
    all_movies = []
    for movie in list:
        all_final = MovieDescription(movie)
        # print(all_final)
        all_movies.append(all_final)


    return all_movies


if __name__ == "__main__":
    print(get_all_final_movies(get_top_movies(11, 1)))
