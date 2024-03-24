#!/usr/bin/env python3

import glob
import numpy as np
import os
import pypdf


n_days = 10
difficulty = 1
tags = ["幼兒園", "學前班"]

assert difficulty < len(tags)

with open("base.tex", "r") as f_in:
    base = f_in.read()

def get_number(n, p):
    number= np.random.choice(
      n,
      1,
      p=p,
    )
    return int(number)

def make_add_less_ten():
    n = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    p = np.array([1, 5, 4, 3, 2, 1, 2, 2, 1, 1], dtype=float)
    p = p / np.sum(p)
    a = get_number(n , p)
    b = get_number(n , p)
    while 10 < a + b:
        a = get_number(n, p)
        b = get_number(n, p)
 
    return f"{a} + {b} = "

def make_sub_greater_zero():
    na = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    pa = np.array([1, 5, 4, 3, 2, 2, 2, 2, 1, 1], dtype=float)
    pa = pa / np.sum(pa)

    nb = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    pb = np.array([1, 5, 4, 3, 2, 2, 2, 2, 1, 1], dtype=float)
    pb = pb / np.sum(pb)

    a = get_number(na, pa)
    b = get_number(nb, pb)
    while a - b < 0:
        a = get_number(na, pa)
        b = get_number(nb, pb)

    return f"{a} - {b} = "

def make_add_sub_less_ten():
    p_add = 0.7
    exercise = ""
    if np.random.uniform() < p_add:
        exercise = make_add_less_ten()
    else:
        exercise = make_sub_greater_zero()
    return exercise

def make_exercise(difficulty):
    exercise = ""
    if difficulty == 0:
        exercise = make_add_less_ten()
    elif difficulty == 1:
        exercise = make_add_sub_less_ten()
    return exercise

def make_exercises(n, difficulty):
    exercises = []
    for _ in range(n):
        exercise = make_exercise(difficulty)
        while exercise in exercises:
            exercise = make_exercise(difficulty)
        exercises.append(exercise)
    return exercises

for n in range(n_days):
    content = base

    content = content.replace("§級別", tags[difficulty])

    exercises = make_exercises(30, difficulty)
    for i, exercise in enumerate(exercises):
        content = content.replace(f"§{i+1:02}", exercise)

    with open(f"meiri{n}.tex", "w") as f_out:
        f_out.write(content)

    os.system(f"xelatex meiri{n}.tex")

merger = pypdf.PdfWriter()

for i in range(n_days):
    filename = f"meiri{i}.pdf"
    merger.append(filename)
    old_files = glob.glob(f"meiri{i}.*")
    for f in old_files:
        os.remove(f)

merger.write(f"{tags[difficulty]}.pdf")
merger.close()
