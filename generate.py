#!/usr/bin/env python3

import glob
import numpy as np
import os
import pypdf


n_days = 10

with open("base.tex", "r") as f_in:
    base = f_in.read()

def get_number():
    n = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    p = np.array([1, 5, 4, 3, 2, 1, 2, 2, 1, 1], dtype=float)
    p = p / np.sum(p)
    number= np.random.choice(
      n,
      1,
      p=p,
    )
    return int(number)

def make_exercise():
    a = get_number()
    b = get_number()
    while 10 < a + b:
        a = get_number()
        b = get_number()
 
    return f"{a} + {b} = "

def make_exercises(n):
    exercises = []
    for _ in range(n):
        exercise = make_exercise()
        while exercise in exercises:
            exercise = make_exercise()
        exercises.append(exercise)
    return exercises

for n in range(n_days):
    content = base

    content = content.replace("§級別", "學前班")

    exercises = make_exercises(30)
    for i, exercise in enumerate(exercises):
        excerize = make_exercise()
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

merger.write("meiri.pdf")
merger.close()
