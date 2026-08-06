import tkinter as tk
import math

# ─── COLORS ─────────────────────────────────────────
BG        = "#0f0f11"
BG2       = "#1c1c1e"
BG3       = "#2c2c2e"
DISPLAY   = "#1a1a1e"
BTN_NUM   = "#333335"
BTN_OP    = "#ff9f0a"
BTN_FN    = "#636366"
FG        = "#ffffff"
FG_DIM    = "#888888"
ACCENT    = "#ff9f0a"
HOVER_NUM = "#444446"
HOVER_OP  = "#ffb340"
HOVER_FN  = "#7a7a7e"

def style_button(btn, kind="num"):
    colors = {
        "num": (BTN_NUM, HOVER_NUM),
        "op":  (BTN_OP,  HOVER_OP),
        "fn":  (BTN_FN,  HOVER_FN),
    }
    bg, hov = colors[kind]
    btn.config(bg=bg, fg=FG, activebackground=bg, activeforeground=FG,
               relief="flat", bd=0, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg=hov))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

def labeled_entry(parent, label, var, hint=""):
    tk.Label(parent, text=label, bg=BG2, fg=FG_DIM,
             font=("Helvetica", 12)).pack(anchor="w")
    e = tk.Entry(parent, textvariable=var, font=("Helvetica", 16),
                 bg=BG3, fg=FG, bd=0, insertbackground=ACCENT)
    e.pack(fill="x", ipady=8, pady=(2,10))
    return e

def result_label(parent, text="—", size=22):
    lbl = tk.Label(parent, text=text, bg=BG2, fg=ACCENT,
                   font=("Helvetica", size, "bold"))
    lbl.pack(pady=4)
    return lbl

def accent_button(parent, text, cmd):
    btn = tk.Button(parent, text=text, font=("Helvetica", 13),
                    bg=ACCENT, fg="#000", relief="flat", bd=0,
                    activebackground=HOVER_OP, activeforeground="#000",
                    cursor="hand2", command=cmd)
    btn.pack(fill="x", ipady=10, pady=(0,12))
    btn.bind("<Enter>", lambda e: btn.config(bg=HOVER_OP))
    btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))
    return btn

def unit_toggle(parent, var, opt1, opt2):
    frm = tk.Frame(parent, bg=BG3)
    frm.pack(fill="x", pady=(0,10))
    for opt in [opt1, opt2]:
        b = tk.Button(frm, text=opt, font=("Helvetica", 11),
                      relief="flat", bd=0, cursor="hand2", padx=12, pady=4,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda o=opt: [var.set(o), refresh_toggle(frm, var, opt1, opt2)])
        b.pack(side="left", expand=True, fill="x")
    refresh_toggle(frm, var, opt1, opt2)
    return frm

def refresh_toggle(frm, var, opt1, opt2):
    for i, opt in enumerate([opt1, opt2]):
        btn = frm.winfo_children()[i]
        is_sel = var.get() == opt
        btn.config(bg=ACCENT if is_sel else BG3,
                   fg="#000" if is_sel else FG)

# ─── FITNESS SUB-TABS ───────────────────────────────
def build_fitness(parent):
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="both", expand=True)

    sub_tabs = [
        ("BMI",        build_bmi),
        ("Calories",   build_calories),
        ("Protein",    build_protein),
        ("Macros",     build_macros),
        ("Water",      build_water),
        ("Body Fat",   build_bodyfat),
        ("Ideal Wt",   build_idealweight),
        ("1RM",        build_1rm),
        ("HR Zones",   build_herzones),
    ]

    # Sub-tab bar
    sub_bar = tk.Frame(outer, bg="#111113")
    sub_bar.pack(fill="x")

    sub_contents  = []
    sub_btns      = []
    sub_indicators= []
    active_sub    = tk.IntVar(value=0)

    def switch_sub(i):
        active_sub.set(i)
        for j, c in enumerate(sub_contents):
            c.pack(fill="both", expand=True) if j == i else c.pack_forget()
        for j, (btn, ind) in enumerate(zip(sub_btns, sub_indicators)):
            if j == i:
                btn.config(fg=ACCENT, bg=BG2, font=("Helvetica", 8, "bold"),
                           activebackground=BG2, activeforeground=ACCENT)
                ind.config(bg=ACCENT)
            else:
                btn.config(fg=FG_DIM, bg="#111113", font=("Helvetica", 8),
                           activebackground="#111113", activeforeground=FG_DIM)
                ind.config(bg="#111113")

    for i, (name, builder) in enumerate(sub_tabs):
        col = tk.Frame(sub_bar, bg="#111113")
        col.pack(side="left", expand=True, fill="x")

        btn = tk.Button(col, text=name, font=("Helvetica", 8),
                        bg="#111113", fg=FG_DIM, relief="flat", bd=0,
                        cursor="hand2", pady=6,
                        activebackground="#111113",
                        activeforeground=ACCENT,
                        command=lambda x=i: switch_sub(x))
        btn.pack(fill="x")
        btn.bind("<Enter>", lambda e, b=btn, x=i:
                 b.config(fg=ACCENT) if active_sub.get() != x else None)
        btn.bind("<Leave>", lambda e, b=btn, x=i:
                 b.config(fg=FG_DIM) if active_sub.get() != x else None)
        sub_btns.append(btn)

        ind = tk.Frame(col, bg="#111113", height=2)
        ind.pack(fill="x")
        sub_indicators.append(ind)

        c = tk.Frame(outer, bg=BG2)
        sub_contents.append(c)
        builder(c)

    switch_sub(0)

# ─── BMI ────────────────────────────────────────────
def build_bmi(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    unit  = tk.StringVar(value="kg/cm")
    h_var = tk.StringVar()
    w_var = tk.StringVar()
    res   = tk.StringVar(value="—")
    cat   = tk.StringVar()

    tk.Label(frame, text="BMI Calculator", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,8))
    unit_toggle(frame, unit, "kg/cm", "lbs/in")

    tk.Label(frame, text="Height:", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 12)).pack(anchor="w")
    tk.Entry(frame, textvariable=h_var, font=("Helvetica", 16),
             bg=BG3, fg=FG, bd=0, insertbackground=ACCENT).pack(
             fill="x", ipady=8, pady=(2,10))

    tk.Label(frame, text="Weight:", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 12)).pack(anchor="w")
    tk.Entry(frame, textvariable=w_var, font=("Helvetica", 16),
             bg=BG3, fg=FG, bd=0, insertbackground=ACCENT).pack(
             fill="x", ipady=8, pady=(2,10))

    res_lbl = tk.Label(frame, textvariable=res, bg=BG2, fg=ACCENT,
                       font=("Helvetica", 28, "bold"))
    res_lbl.pack()
    cat_lbl = tk.Label(frame, textvariable=cat, bg=BG2, fg=FG,
                       font=("Helvetica", 13))
    cat_lbl.pack(pady=4)

    canvas = tk.Canvas(frame, bg=BG3, height=12, bd=0, highlightthickness=0)
    canvas.pack(fill="x", pady=8)

    def calc():
        try:
            if unit.get() == "kg/cm":
                h = float(h_var.get()) / 100
                w = float(w_var.get())
            else:
                h = float(h_var.get()) * 0.0254
                w = float(w_var.get()) * 0.453592
            bmi = w / h**2
            res.set(f"BMI: {round(bmi,1)}")
            if bmi < 18.5:
                cat.set("⚠️ Underweight"); cat_lbl.config(fg="#5ac8fa"); c="#5ac8fa"; bv=25
            elif bmi < 25:
                cat.set("✅ Normal weight"); cat_lbl.config(fg="#30d158"); c="#30d158"; bv=50
            elif bmi < 30:
                cat.set("⚠️ Overweight"); cat_lbl.config(fg=ACCENT); c=ACCENT; bv=75
            else:
                cat.set("🔴 Obese"); cat_lbl.config(fg="#ff453a"); c="#ff453a"; bv=95
            canvas.delete("all")
            cw = canvas.winfo_width() or 400
            canvas.create_rectangle(0,0,cw,12,fill=BG3,outline="")
            canvas.create_rectangle(0,0,int(bv/100*cw),12,fill=c,outline="")
        except:
            res.set("Error"); cat.set("")

    accent_button(frame, "Calculate BMI", calc)
    tk.Label(frame, text="<18.5 Under  |  18.5-24.9 Normal  |  25-29.9 Over  |  ≥30 Obese",
             bg=BG2, fg=FG_DIM, font=("Helvetica", 9)).pack()

# ─── CALORIES (TDEE) ────────────────────────────────
def build_calories(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    unit    = tk.StringVar(value="kg/cm")
    age_v   = tk.StringVar()
    h_v     = tk.StringVar()
    w_v     = tk.StringVar()
    gender  = tk.StringVar(value="Male")
    activity= tk.StringVar(value="Moderate")
    goal    = tk.StringVar(value="Maintain")
    res     = tk.StringVar(value="—")

    tk.Label(frame, text="Daily Calories (TDEE)", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,6))
    unit_toggle(frame, unit, "kg/cm", "lbs/in")

    # Gender
    gf = tk.Frame(frame, bg=BG2)
    gf.pack(fill="x", pady=(0,8))
    for g in ["Male","Female"]:
        b = tk.Button(gf, text=g, font=("Helvetica", 11), relief="flat", bd=0,
                      cursor="hand2", padx=12, pady=4,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda x=g: [gender.set(x),
                          [btn.config(bg=ACCENT if btn["text"]==x else BG3,
                                      fg="#000" if btn["text"]==x else FG)
                           for btn in gf.winfo_children()]])
        b.pack(side="left", expand=True, fill="x")
        b.config(bg=ACCENT if g=="Male" else BG3, fg="#000" if g=="Male" else FG)

    for lbl, var in [("Age:", age_v), ("Height:", h_v), ("Weight:", w_v)]:
        tk.Label(frame, text=lbl, bg=BG2, fg=FG_DIM,
                 font=("Helvetica", 11)).pack(anchor="w")
        tk.Entry(frame, textvariable=var, font=("Helvetica", 14),
                 bg=BG3, fg=FG, bd=0, insertbackground=ACCENT).pack(
                 fill="x", ipady=6, pady=(1,6))

    # Activity
    tk.Label(frame, text="Activity Level:", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 11)).pack(anchor="w")
    act_frame = tk.Frame(frame, bg=BG2)
    act_frame.pack(fill="x", pady=(2,8))
    act_levels = ["Sedentary","Light","Moderate","Active","Very Active"]
    for a in act_levels:
        b = tk.Button(act_frame, text=a, font=("Helvetica", 9), relief="flat", bd=0,
                      cursor="hand2", padx=4, pady=4,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda x=a: [activity.set(x),
                          [btn.config(bg=ACCENT if btn["text"]==x else BG3,
                                      fg="#000" if btn["text"]==x else FG)
                           for btn in act_frame.winfo_children()]])
        b.pack(side="left", expand=True, fill="x")
        b.config(bg=ACCENT if a=="Moderate" else BG3,
                 fg="#000" if a=="Moderate" else FG)

    # Goal
    tk.Label(frame, text="Goal:", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 11)).pack(anchor="w")
    goal_frame = tk.Frame(frame, bg=BG2)
    goal_frame.pack(fill="x", pady=(2,8))
    for g in ["Lose Weight","Maintain","Gain Muscle"]:
        b = tk.Button(goal_frame, text=g, font=("Helvetica", 9), relief="flat", bd=0,
                      cursor="hand2", padx=4, pady=4,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda x=g: [goal.set(x),
                          [btn.config(bg=ACCENT if btn["text"]==x else BG3,
                                      fg="#000" if btn["text"]==x else FG)
                           for btn in goal_frame.winfo_children()]])
        b.pack(side="left", expand=True, fill="x")
        b.config(bg=ACCENT if g=="Maintain" else BG3,
                 fg="#000" if g=="Maintain" else FG)

    res_lbl = tk.Label(frame, textvariable=res, bg=BG2, fg=ACCENT,
                       font=("Helvetica", 22, "bold"))
    res_lbl.pack(pady=4)

    def calc():
        try:
            age = float(age_v.get())
            if unit.get() == "kg/cm":
                h = float(h_v.get()); w = float(w_v.get())
            else:
                h = float(h_v.get()) * 2.54; w = float(w_v.get()) * 0.453592
            if gender.get() == "Male":
                bmr = 10*w + 6.25*h - 5*age + 5
            else:
                bmr = 10*w + 6.25*h - 5*age - 161
            mult = {"Sedentary":1.2,"Light":1.375,"Moderate":1.55,
                    "Active":1.725,"Very Active":1.9}[activity.get()]
            tdee = bmr * mult
            adj = {"Lose Weight":-500,"Maintain":0,"Gain Muscle":+300}[goal.get()]
            final = tdee + adj
            res.set(f"{round(final)} kcal/day")
        except:
            res.set("Error")

    accent_button(frame, "Calculate", calc)

# ─── PROTEIN ────────────────────────────────────────
def build_protein(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    unit  = tk.StringVar(value="kg")
    w_var = tk.StringVar()
    goal  = tk.StringVar(value="Build Muscle")
    res   = tk.StringVar(value="—")

    tk.Label(frame, text="Daily Protein", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,8))
    unit_toggle(frame, unit, "kg", "lbs")

    labeled_entry(frame, "Body Weight:", w_var)

    tk.Label(frame, text="Goal:", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 12)).pack(anchor="w")
    gf = tk.Frame(frame, bg=BG2)
    gf.pack(fill="x", pady=(2,12))
    goals = ["Lose Fat", "Maintain", "Build Muscle", "Athlete"]
    for g in goals:
        b = tk.Button(gf, text=g, font=("Helvetica", 10), relief="flat", bd=0,
                      cursor="hand2", padx=6, pady=6,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda x=g: [goal.set(x),
                          [btn.config(bg=ACCENT if btn["text"]==x else BG3,
                                      fg="#000" if btn["text"]==x else FG)
                           for btn in gf.winfo_children()]])
        b.pack(side="left", expand=True, fill="x")
        b.config(bg=ACCENT if g=="Build Muscle" else BG3,
                 fg="#000" if g=="Build Muscle" else FG)

    tk.Label(frame, textvariable=res, bg=BG2, fg=ACCENT,
             font=("Helvetica", 26, "bold")).pack(pady=8)

    def calc():
        try:
            w = float(w_var.get())
            if unit.get() == "lbs": w = w * 0.453592
            mult = {"Lose Fat":1.8,"Maintain":1.6,
                    "Build Muscle":2.2,"Athlete":2.6}[goal.get()]
            res.set(f"{round(w * mult)}g / day")
        except:
            res.set("Error")

    accent_button(frame, "Calculate", calc)

    tk.Label(frame, text="Lose Fat: 1.8g/kg  |  Maintain: 1.6g/kg\n"
             "Build Muscle: 2.2g/kg  |  Athlete: 2.6g/kg",
             bg=BG2, fg=FG_DIM, font=("Helvetica", 9),
             justify="center").pack(pady=4)

# ─── MACROS ─────────────────────────────────────────
def build_macros(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    cal_var = tk.StringVar()
    goal    = tk.StringVar(value="Balanced")
    p_res   = tk.StringVar(value="Protein: —")
    c_res   = tk.StringVar(value="Carbs: —")
    f_res   = tk.StringVar(value="Fat: —")

    tk.Label(frame, text="Macros Calculator", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,8))

    labeled_entry(frame, "Daily Calories (kcal):", cal_var)

    tk.Label(frame, text="Goal:", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 12)).pack(anchor="w")
    gf = tk.Frame(frame, bg=BG2)
    gf.pack(fill="x", pady=(2,12))

    # protein%, carb%, fat%
    macro_splits = {
        "Lose Fat":     (0.40, 0.35, 0.25),
        "Balanced":     (0.30, 0.40, 0.30),
        "Build Muscle": (0.35, 0.45, 0.20),
        "Keto":         (0.30, 0.05, 0.65),
        "Endurance":    (0.20, 0.55, 0.25),
    }
    for g in macro_splits:
        b = tk.Button(gf, text=g, font=("Helvetica", 9), relief="flat", bd=0,
                      cursor="hand2", padx=4, pady=6,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda x=g: [goal.set(x),
                          [btn.config(bg=ACCENT if btn["text"]==x else BG3,
                                      fg="#000" if btn["text"]==x else FG)
                           for btn in gf.winfo_children()]])
        b.pack(side="left", expand=True, fill="x")
        b.config(bg=ACCENT if g=="Balanced" else BG3,
                 fg="#000" if g=="Balanced" else FG)

    # Results
    res_frame = tk.Frame(frame, bg=BG3)
    res_frame.pack(fill="x", pady=8)
    for var, color in [(p_res,"#30d158"),(c_res,"#5ac8fa"),(f_res,ACCENT)]:
        row = tk.Frame(res_frame, bg=BG3)
        row.pack(fill="x", padx=12, pady=6)
        tk.Label(row, textvariable=var, bg=BG3, fg=color,
                 font=("Helvetica", 16, "bold")).pack(side="left")

    def calc():
        try:
            cals = float(cal_var.get())
            p_pct, c_pct, f_pct = macro_splits[goal.get()]
            p_res.set(f"Protein:  {round(cals * p_pct / 4)}g")
            c_res.set(f"Carbs:    {round(cals * c_pct / 4)}g")
            f_res.set(f"Fat:      {round(cals * f_pct / 9)}g")
        except:
            p_res.set("Protein: Error")

    accent_button(frame, "Calculate Macros", calc)
    tk.Label(frame, text="Protein & Carbs = 4 kcal/g  |  Fat = 9 kcal/g",
             bg=BG2, fg=FG_DIM, font=("Helvetica", 9)).pack()

# ─── WATER ──────────────────────────────────────────
def build_water(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    unit     = tk.StringVar(value="kg")
    w_var    = tk.StringVar()
    activity = tk.StringVar(value="Moderate")
    res      = tk.StringVar(value="—")

    tk.Label(frame, text="Daily Water Intake", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,8))
    unit_toggle(frame, unit, "kg", "lbs")
    labeled_entry(frame, "Body Weight:", w_var)

    tk.Label(frame, text="Activity Level:", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 12)).pack(anchor="w")
    af = tk.Frame(frame, bg=BG2)
    af.pack(fill="x", pady=(2,12))
    for a in ["Low","Moderate","High","Athlete"]:
        b = tk.Button(af, text=a, font=("Helvetica", 10), relief="flat", bd=0,
                      cursor="hand2", padx=6, pady=6,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda x=a: [activity.set(x),
                          [btn.config(bg=ACCENT if btn["text"]==x else BG3,
                                      fg="#000" if btn["text"]==x else FG)
                           for btn in af.winfo_children()]])
        b.pack(side="left", expand=True, fill="x")
        b.config(bg=ACCENT if a=="Moderate" else BG3,
                 fg="#000" if a=="Moderate" else FG)

    tk.Label(frame, textvariable=res, bg=BG2, fg=ACCENT,
             font=("Helvetica", 26, "bold")).pack(pady=12)

    def calc():
        try:
            w = float(w_var.get())
            if unit.get() == "lbs": w = w * 0.453592
            mult = {"Low":30,"Moderate":35,"High":40,"Athlete":45}[activity.get()]
            ml = w * mult
            res.set(f"{round(ml)} ml  ({round(ml/1000, 1)} L)")
        except:
            res.set("Error")

    accent_button(frame, "Calculate", calc)

# ─── BODY FAT ───────────────────────────────────────
def build_bodyfat(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    unit   = tk.StringVar(value="kg/cm")
    gender = tk.StringVar(value="Male")
    neck_v = tk.StringVar()
    waist_v= tk.StringVar()
    hip_v  = tk.StringVar()
    h_v    = tk.StringVar()
    res    = tk.StringVar(value="—")
    cat    = tk.StringVar()

    tk.Label(frame, text="Body Fat % (Navy Method)", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,6))
    unit_toggle(frame, unit, "kg/cm", "lbs/in")

    gf = tk.Frame(frame, bg=BG2)
    gf.pack(fill="x", pady=(0,8))
    for g in ["Male","Female"]:
        b = tk.Button(gf, text=g, font=("Helvetica", 11), relief="flat", bd=0,
                      cursor="hand2", padx=12, pady=4,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda x=g: [gender.set(x), update_hip(),
                          [btn.config(bg=ACCENT if btn["text"]==x else BG3,
                                      fg="#000" if btn["text"]==x else FG)
                           for btn in gf.winfo_children()]])
        b.pack(side="left", expand=True, fill="x")
        b.config(bg=ACCENT if g=="Male" else BG3, fg="#000" if g=="Male" else FG)

    for lbl, var in [("Neck (cm/in):", neck_v),
                     ("Waist (cm/in):", waist_v),
                     ("Height (cm/in):", h_v)]:
        tk.Label(frame, text=lbl, bg=BG2, fg=FG_DIM,
                 font=("Helvetica", 11)).pack(anchor="w")
        tk.Entry(frame, textvariable=var, font=("Helvetica", 14),
                 bg=BG3, fg=FG, bd=0, insertbackground=ACCENT).pack(
                 fill="x", ipady=6, pady=(1,6))

    hip_lbl = tk.Label(frame, text="Hip (cm/in) — Women only:", bg=BG2,
                       fg=FG_DIM, font=("Helvetica", 11))
    hip_entry = tk.Entry(frame, textvariable=hip_v, font=("Helvetica", 14),
                         bg=BG3, fg=FG, bd=0, insertbackground=ACCENT)

    def update_hip():
        if gender.get() == "Female":
            hip_lbl.pack(anchor="w")
            hip_entry.pack(fill="x", ipady=6, pady=(1,6))
        else:
            hip_lbl.pack_forget()
            hip_entry.pack_forget()

    tk.Label(frame, textvariable=res, bg=BG2, fg=ACCENT,
             font=("Helvetica", 26, "bold")).pack(pady=4)
    tk.Label(frame, textvariable=cat, bg=BG2, fg=FG_DIM,
             font=("Helvetica", 12)).pack()

    def calc():
        try:
            def to_cm(v): return float(v) if unit.get()=="kg/cm" else float(v)*2.54
            neck=to_cm(neck_v.get()); waist=to_cm(waist_v.get()); h=to_cm(h_v.get())
            if gender.get()=="Male":
                bf = 495/(1.0324 - 0.19077*math.log10(waist-neck) + 0.15456*math.log10(h)) - 450
            else:
                hip=to_cm(hip_v.get())
                bf = 495/(1.29579 - 0.35004*math.log10(waist+hip-neck) + 0.22100*math.log10(h)) - 450
            res.set(f"{round(bf, 1)}%")
            if gender.get()=="Male":
                c = "Essential" if bf<6 else "Athlete" if bf<14 else "Fitness" if bf<18 else "Average" if bf<25 else "Obese"
            else:
                c = "Essential" if bf<14 else "Athlete" if bf<21 else "Fitness" if bf<25 else "Average" if bf<32 else "Obese"
            cat.set(c)
        except:
            res.set("Error"); cat.set("")

    accent_button(frame, "Calculate Body Fat", calc)
    update_hip()

# ─── IDEAL WEIGHT ───────────────────────────────────
def build_idealweight(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    unit   = tk.StringVar(value="cm")
    h_var  = tk.StringVar()
    gender = tk.StringVar(value="Male")
    res    = tk.StringVar(value="—")

    tk.Label(frame, text="Ideal Body Weight", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,8))
    unit_toggle(frame, unit, "cm", "inches")

    gf = tk.Frame(frame, bg=BG2)
    gf.pack(fill="x", pady=(0,8))
    for g in ["Male","Female"]:
        b = tk.Button(gf, text=g, font=("Helvetica", 11), relief="flat", bd=0,
                      cursor="hand2", padx=12, pady=4,
                      activebackground=ACCENT, activeforeground="#000",
                      command=lambda x=g: [gender.set(x),
                          [btn.config(bg=ACCENT if btn["text"]==x else BG3,
                                      fg="#000" if btn["text"]==x else FG)
                           for btn in gf.winfo_children()]])
        b.pack(side="left", expand=True, fill="x")
        b.config(bg=ACCENT if g=="Male" else BG3, fg="#000" if g=="Male" else FG)

    labeled_entry(frame, "Height:", h_var)

    tk.Label(frame, textvariable=res, bg=BG2, fg=ACCENT,
             font=("Helvetica", 22, "bold")).pack(pady=8)

    def calc():
        try:
            h = float(h_var.get())
            if unit.get() == "cm": h_in = h / 2.54
            else: h_in = h
            over = h_in - 60
            if gender.get() == "Male":
                devine = 50 + 2.3 * over
                robinson = 52 + 1.9 * over
            else:
                devine = 45.5 + 2.3 * over
                robinson = 49 + 1.7 * over
            avg = (devine + robinson) / 2
            res.set(f"{round(avg, 1)} kg  ({round(avg*2.20462, 1)} lbs)")
        except:
            res.set("Error")

    accent_button(frame, "Calculate", calc)
    tk.Label(frame, text="Based on Devine & Robinson formulas",
             bg=BG2, fg=FG_DIM, font=("Helvetica", 9)).pack()

# ─── 1RM ────────────────────────────────────────────
def build_1rm(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    unit   = tk.StringVar(value="kg")
    w_var  = tk.StringVar()
    r_var  = tk.StringVar()

    tk.Label(frame, text="1RM Calculator", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,8))
    unit_toggle(frame, unit, "kg", "lbs")

    labeled_entry(frame, "Weight lifted:", w_var)
    labeled_entry(frame, "Reps performed:", r_var)

    res_frame = tk.Frame(frame, bg=BG3)
    res_frame.pack(fill="x", pady=8)

    rows = []
    for pct in [100,95,90,85,80,75,70]:
        row = tk.Frame(res_frame, bg=BG3)
        row.pack(fill="x", padx=12, pady=3)
        tk.Label(row, text=f"{pct}%", bg=BG3, fg=FG_DIM,
                 font=("Helvetica", 11)).pack(side="left")
        lbl = tk.Label(row, text="—", bg=BG3, fg=ACCENT if pct==100 else FG,
                       font=("Helvetica", 13, "bold" if pct==100 else "normal"))
        lbl.pack(side="right")
        rows.append((pct, lbl))

    def calc():
        try:
            w = float(w_var.get())
            r = float(r_var.get())
            one_rm = w * (1 + r/30)
            u = unit.get()
            for pct, lbl in rows:
                val = round(one_rm * pct/100, 1)
                lbl.config(text=f"{val} {u}")
        except:
            for _, lbl in rows: lbl.config(text="Error")

    accent_button(frame, "Calculate 1RM", calc)

# ─── HEART RATE ZONES ───────────────────────────────
def build_herzones(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    age_var = tk.StringVar()
    hr_var  = tk.StringVar()

    tk.Label(frame, text="Heart Rate Zones", bg=BG2, fg=FG,
             font=("Helvetica", 16, "bold")).pack(pady=(0,8))

    labeled_entry(frame, "Age:", age_var)
    tk.Label(frame, text="Resting HR (optional):", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 12)).pack(anchor="w")
    tk.Entry(frame, textvariable=hr_var, font=("Helvetica", 16),
             bg=BG3, fg=FG, bd=0, insertbackground=ACCENT).pack(
             fill="x", ipady=8, pady=(2,10))

    zones_frame = tk.Frame(frame, bg=BG3)
    zones_frame.pack(fill="x", pady=4)

    zone_colors = ["#5ac8fa","#30d158","#ff9f0a","#ff6b35","#ff453a"]
    zone_labels = []

    for i, (name, color) in enumerate(zip(
        ["Z1 — Warm Up","Z2 — Fat Burn","Z3 — Cardio","Z4 — Hard","Z5 — Max"],
        zone_colors
    )):
        row = tk.Frame(zones_frame, bg=BG3)
        row.pack(fill="x", padx=10, pady=4)
        tk.Label(row, text=name, bg=BG3, fg=color,
                 font=("Helvetica", 11, "bold"), width=18, anchor="w").pack(side="left")
        lbl = tk.Label(row, text="—", bg=BG3, fg=FG,
                       font=("Helvetica", 11))
        lbl.pack(side="right")
        zone_labels.append(lbl)

    def calc():
        try:
            age = float(age_var.get())
            max_hr = 220 - age
            try:
                rhr = float(hr_var.get())
                hrr = max_hr - rhr
                zones = [
                    (rhr + hrr*0.50, rhr + hrr*0.60),
                    (rhr + hrr*0.60, rhr + hrr*0.70),
                    (rhr + hrr*0.70, rhr + hrr*0.80),
                    (rhr + hrr*0.80, rhr + hrr*0.90),
                    (rhr + hrr*0.90, max_hr),
                ]
            except:
                zones = [
                    (max_hr*0.50, max_hr*0.60),
                    (max_hr*0.60, max_hr*0.70),
                    (max_hr*0.70, max_hr*0.80),
                    (max_hr*0.80, max_hr*0.90),
                    (max_hr*0.90, max_hr),
                ]
            for i, (lo, hi) in enumerate(zones):
                zone_labels[i].config(text=f"{round(lo)} – {round(hi)} bpm")
        except:
            for lbl in zone_labels: lbl.config(text="Error")

    accent_button(frame, "Calculate Zones", calc)

# ─── TAB 1: BASIC + SCIENTIFIC ──────────────────────
def build_calculator(parent):
    expression = tk.StringVar(value="")
    sci_visible = tk.BooleanVar(value=False)
    history = []

    def press(val): expression.set(expression.get() + str(val))
    def clear(): expression.set("")
    def backspace(): expression.set(expression.get()[:-1])

    def calculate():
        try:
            expr = expression.get().replace("×","*").replace("÷","/").replace("−","-").replace("^","**")
            result = eval(expr, {"__builtins__": {}}, {
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "sqrt": math.sqrt, "log": math.log10,
                "ln": math.log, "pi": math.pi, "e": math.e,
                "abs": abs, "factorial": math.factorial,
            })
            res = str(round(result, 10))
            if '.' in res: res = res.rstrip('0').rstrip('.')
            history.append(f"{expression.get()} = {res}")
            if len(history) > 5: history.pop(0)
            update_history()
            expression.set(res)
        except: expression.set("Error")

    def toggle_sci():
        if sci_visible.get():
            sci_frame.pack_forget()
            sci_visible.set(False)
            sci_btn.config(text="  Scientific  ▼")
        else:
            sci_frame.pack(fill="x", padx=12, before=btn_frame)
            sci_visible.set(True)
            sci_btn.config(text="  Scientific  ▲")

    def update_history():
        hist_text.config(state="normal")
        hist_text.delete(1.0, tk.END)
        for h in reversed(history): hist_text.insert(tk.END, h + "\n")
        hist_text.config(state="disabled")

    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True)

    disp_frame = tk.Frame(frame, bg=DISPLAY, padx=16, pady=12)
    disp_frame.pack(fill="x", padx=12, pady=(12,6))
    tk.Label(disp_frame, text="Basic Calculator", bg=DISPLAY,
             fg=FG_DIM, font=("Helvetica", 10)).pack(anchor="e")
    tk.Entry(disp_frame, textvariable=expression, font=("Helvetica", 32),
             justify="right", bg=DISPLAY, fg=FG, bd=0,
             insertbackground=ACCENT).pack(fill="x")

    sci_btn = tk.Button(frame, text="  Scientific  ▼", font=("Helvetica", 11),
                        bg=BG3, fg=ACCENT, relief="flat", bd=0,
                        activebackground=BG3, activeforeground=ACCENT,
                        cursor="hand2", command=toggle_sci, anchor="w")
    sci_btn.pack(fill="x", padx=12, pady=(0,4))
    sci_btn.bind("<Enter>", lambda e: sci_btn.config(bg="#3a3a3c"))
    sci_btn.bind("<Leave>", lambda e: sci_btn.config(bg=BG3))

    btn_frame = tk.Frame(frame, bg=BG2)
    btn_frame.pack(padx=12, pady=8)

    for r, row in enumerate([["C","⌫","%","÷"],["7","8","9","×"],
                              ["4","5","6","−"],["1","2","3","+"],["00","0",".","="]]):
        for c, btn in enumerate(row):
            if btn=="C":    cmd,kind=clear,"fn"
            elif btn=="⌫": cmd,kind=backspace,"fn"
            elif btn=="=":  cmd,kind=calculate,"op"
            elif btn=="÷":  cmd,kind=lambda:press("/"),"op"
            elif btn=="×":  cmd,kind=lambda:press("*"),"op"
            elif btn=="−":  cmd,kind=lambda:press("-"),"op"
            elif btn=="+":  cmd,kind=lambda:press("+"),"op"
            elif btn=="%":  cmd,kind=lambda:press("%"),"fn"
            else:           cmd,kind=lambda b=btn:press(b),"num"
            b = tk.Button(btn_frame, text=btn, font=("Helvetica", 20),
                          width=4, height=2, command=cmd)
            style_button(b, kind)
            b.grid(row=r, column=c, padx=4, pady=4)

    sci_frame = tk.Frame(frame, bg=BG2)
    for r, row in enumerate([["sin(","cos(","tan(","log(","ln("],
                              ["sqrt(","π","e","^","abs("],
                              ["(",")", "n!","1/",""]]):
        for c, btn in enumerate(row):
            if btn=="": continue
            val = "pi" if btn=="π" else "factorial(" if btn=="n!" else btn
            b = tk.Button(sci_frame, text=btn, font=("Helvetica", 12),
                          width=6, height=1, bg=BG3, fg=ACCENT,
                          relief="flat", bd=0, cursor="hand2",
                          activebackground=BG3, activeforeground=ACCENT,
                          command=lambda v=val: press(v))
            b.grid(row=r, column=c, padx=2, pady=2)
            b.bind("<Enter>", lambda e, x=b: x.config(bg="#3a3a3c"))
            b.bind("<Leave>", lambda e, x=b: x.config(bg=BG3))

    hist_frame = tk.Frame(frame, bg=BG3)
    hist_frame.pack(fill="x", padx=12, pady=(0,12))
    tk.Label(hist_frame, text="History", bg=BG3, fg=FG_DIM,
             font=("Helvetica", 10)).pack(anchor="w", padx=8, pady=(6,0))
    hist_text = tk.Text(hist_frame, bg=BG3, fg=FG_DIM, font=("Helvetica", 11),
                        height=3, bd=0, state="disabled", wrap="none")
    hist_text.pack(fill="x", padx=8, pady=(0,6))

# ─── TAB 2: CONVERTER ───────────────────────────────
def build_converter(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)

    categories = {
        "📏  Length": {
            "km → miles": lambda x: x*0.621371, "miles → km": lambda x: x*1.60934,
            "m → feet": lambda x: x*3.28084, "feet → m": lambda x: x*0.3048,
            "cm → inches": lambda x: x*0.393701, "inches → cm": lambda x: x*2.54,
        },
        "⚖️  Weight": {
            "kg → lbs": lambda x: x*2.20462, "lbs → kg": lambda x: x/2.20462,
            "kg → st": lambda x: x*0.157473, "st → kg": lambda x: x/0.157473,
            "lbs → st": lambda x: x*0.0714286, "st → lbs": lambda x: x/0.0714286,
            "g → oz": lambda x: x*0.035274, "oz → g": lambda x: x/0.035274,
        },
        "🌡️  Temperature": {
            "°C → °F": lambda x: x*9/5+32, "°F → °C": lambda x: (x-32)*5/9,
            "°C → K": lambda x: x+273.15, "K → °C": lambda x: x-273.15,
        },
        "📐  Area": {
            "m² → ft²": lambda x: x*10.7639, "ft² → m²": lambda x: x/10.7639,
            "ha → acres": lambda x: x*2.47105, "acres → ha": lambda x: x/2.47105,
        },
        "⚡  Speed": {
            "km/h → mph": lambda x: x*0.621371, "mph → km/h": lambda x: x/0.621371,
            "m/s → km/h": lambda x: x*3.6, "km/h → m/s": lambda x: x/3.6,
            "km/h → kn": lambda x: x*0.539957, "kn → km/h": lambda x: x/0.539957,
            "mph → kn": lambda x: x*0.868976, "kn → mph": lambda x: x/0.868976,
        },
        "💾  Data": {
            "MB → GB": lambda x: x/1024, "GB → MB": lambda x: x*1024,
            "GB → TB": lambda x: x/1024, "TB → GB": lambda x: x*1024,
        },
    }

    selected_cat  = tk.StringVar(value=list(categories.keys())[0])
    selected_conv = tk.StringVar()
    input_val     = tk.StringVar()
    result_var    = tk.StringVar(value="—")

    def make_cat_buttons():
        for w in cat_frame.winfo_children(): w.destroy()
        for cat in categories:
            is_sel = selected_cat.get()==cat
            b = tk.Button(cat_frame, text=cat, font=("Helvetica", 11),
                          bg=ACCENT if is_sel else BG3, fg="#000" if is_sel else FG,
                          activebackground=ACCENT if is_sel else BG3,
                          activeforeground="#000" if is_sel else FG,
                          relief="flat", bd=0, cursor="hand2", anchor="w",
                          padx=10, pady=6, command=lambda c=cat: select_cat(c))
            b.pack(fill="x", pady=2)
            if not is_sel:
                b.bind("<Enter>", lambda e, x=b: x.config(bg="#3a3a3c"))
                b.bind("<Leave>", lambda e, x=b: x.config(bg=BG3))

    def make_conv_buttons():
        for w in conv_frame.winfo_children(): w.destroy()
        for conv in categories[selected_cat.get()]:
            is_sel = selected_conv.get()==conv
            b = tk.Button(conv_frame, text=conv, font=("Helvetica", 11),
                          bg=ACCENT if is_sel else BG3, fg="#000" if is_sel else FG,
                          activebackground=ACCENT if is_sel else BG3,
                          activeforeground="#000" if is_sel else FG,
                          relief="flat", bd=0, cursor="hand2", anchor="w",
                          padx=10, pady=5, command=lambda c=conv: select_conv(c))
            b.pack(fill="x", pady=1)
            if not is_sel:
                b.bind("<Enter>", lambda e, x=b: x.config(bg="#3a3a3c"))
                b.bind("<Leave>", lambda e, x=b: x.config(bg=BG3))

    def select_cat(cat):
        selected_cat.set(cat)
        selected_conv.set(list(categories[cat].keys())[0])
        make_cat_buttons(); make_conv_buttons()

    def select_conv(conv):
        selected_conv.set(conv); make_conv_buttons()

    def convert():
        try:
            val = float(input_val.get().replace(",","."))
            result = categories[selected_cat.get()][selected_conv.get()](val)
            result_var.set(f"{round(result,6):,}")
            result_label.config(fg=ACCENT)
        except:
            result_var.set("Error!"); result_label.config(fg="#ff453a")

    left = tk.Frame(frame, bg=BG2, width=160)
    left.pack(side="left", fill="y", padx=(0,10))
    left.pack_propagate(False)
    tk.Label(left, text="Category", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 10)).pack(anchor="w", pady=(0,4))
    cat_frame = tk.Frame(left, bg=BG2)
    cat_frame.pack(fill="both", expand=True)

    right = tk.Frame(frame, bg=BG2)
    right.pack(side="left", fill="both", expand=True)
    tk.Label(right, text="Conversion", bg=BG2, fg=FG_DIM,
             font=("Helvetica", 10)).pack(anchor="w", pady=(0,4))
    conv_frame = tk.Frame(right, bg=BG2)
    conv_frame.pack(fill="x")

    input_frame = tk.Frame(right, bg=BG3, pady=10, padx=10)
    input_frame.pack(fill="x", pady=(12,0))
    tk.Label(input_frame, text="Value:", bg=BG3, fg=FG_DIM,
             font=("Helvetica", 10)).pack(anchor="w")
    entry = tk.Entry(input_frame, textvariable=input_val, font=("Helvetica", 18),
                     bg=DISPLAY, fg=FG, bd=0, insertbackground=ACCENT)
    entry.pack(fill="x", ipady=8, pady=4)
    entry.bind("<Return>", lambda e: convert())

    bc = tk.Button(input_frame, text="Convert →", font=("Helvetica", 13),
                   bg=ACCENT, fg="#000", relief="flat", bd=0,
                   activebackground=HOVER_OP, activeforeground="#000",
                   cursor="hand2", command=convert)
    bc.pack(fill="x", ipady=8)
    bc.bind("<Enter>", lambda e: bc.config(bg=HOVER_OP))
    bc.bind("<Leave>", lambda e: bc.config(bg=ACCENT))

    tk.Label(input_frame, text="Result:", bg=BG3, fg=FG_DIM,
             font=("Helvetica", 10)).pack(anchor="w", pady=(8,0))
    result_label = tk.Label(input_frame, textvariable=result_var, bg=BG3,
                            fg=ACCENT, font=("Helvetica", 24, "bold"))
    result_label.pack(anchor="e")

    selected_conv.set(list(categories[list(categories.keys())[0]].keys())[0])
    make_cat_buttons(); make_conv_buttons()

# ─── TAB 3: PERCENTAGE ──────────────────────────────
def build_percentage(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=16, pady=16)
    frame.columnconfigure([0,1,2,3], weight=1)

    def make_section(title, row_start, labels, calc_fn):
        header = tk.Frame(frame, bg=BG3)
        header.grid(row=row_start, column=0, columnspan=4,
                    sticky="we", pady=(12,4), ipady=6, ipadx=8)
        tk.Label(header, text=title, bg=BG3, fg=ACCENT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w", padx=8)
        vars_ = []
        for col, lbl in enumerate(labels):
            tk.Label(frame, text=lbl, bg=BG2, fg=FG_DIM,
                     font=("Helvetica", 10)).grid(row=row_start+1, column=col,
                                                   sticky="w", padx=4)
            v = tk.StringVar(); vars_.append(v)
            tk.Entry(frame, textvariable=v, font=("Helvetica", 14),
                     bg=BG3, fg=FG, bd=0, insertbackground=ACCENT,
                     width=10).grid(row=row_start+2, column=col, padx=4, ipady=6, sticky="we")
        res_var = tk.StringVar(value="—")
        def do_calc(rv=res_var, vs=vars_):
            try:
                vals = [float(v.get().replace(",",".")) for v in vs]
                rv.set(str(round(calc_fn(*vals), 4)))
                res_lbl.config(fg=ACCENT)
            except:
                rv.set("Error"); res_lbl.config(fg="#ff453a")
        b = tk.Button(frame, text="=", font=("Helvetica", 16),
                      bg=ACCENT, fg="#000", relief="flat", bd=0,
                      activebackground=HOVER_OP, activeforeground="#000",
                      cursor="hand2", width=3, command=do_calc)
        b.grid(row=row_start+2, column=len(labels), padx=4)
        b.bind("<Enter>", lambda e: b.config(bg=HOVER_OP))
        b.bind("<Leave>", lambda e: b.config(bg=ACCENT))
        res_lbl = tk.Label(frame, textvariable=res_var, bg=BG2, fg=ACCENT,
                           font=("Helvetica", 20, "bold"))
        res_lbl.grid(row=row_start+3, column=0, columnspan=4, sticky="e", pady=4, padx=4)

    make_section("X% of Y = ?", 0, ["X (%)","of Y"], lambda a,b: a*b/100)
    make_section("X is what % of Y?", 4, ["X","of Y"], lambda a,b: round(a/b*100,4))
    make_section("Change from X to Y?", 8, ["From X","To Y"], lambda a,b: round((b-a)/a*100,4))

# ─── TAB 5: LOAN ────────────────────────────────────
def build_loan(parent):
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(frame, text="🏦  Loan Calculator", bg=BG2, fg=FG,
             font=("Helvetica", 18, "bold")).pack(pady=(0,16))

    loan_var     = tk.StringVar()
    rate_var     = tk.StringVar()
    months_var   = tk.StringVar()
    monthly_var  = tk.StringVar(value="—")
    total_var    = tk.StringVar(value="—")
    interest_var = tk.StringVar(value="—")

    for label, var in [("Loan amount (€):", loan_var),
                       ("Annual interest rate (%):", rate_var),
                       ("Number of months:", months_var)]:
        tk.Label(frame, text=label, bg=BG2, fg=FG_DIM,
                 font=("Helvetica", 12)).pack(anchor="w")
        tk.Entry(frame, textvariable=var, font=("Helvetica", 18),
                 bg=BG3, fg=FG, bd=0, insertbackground=ACCENT).pack(
                 fill="x", ipady=10, pady=(2,10))

    def calc_loan():
        try:
            P = float(loan_var.get().replace(",","."))
            r = float(rate_var.get().replace(",",".")) / 100 / 12
            n = int(months_var.get())
            monthly = P/n if r==0 else P*r*(1+r)**n/((1+r)**n-1)
            total = monthly*n; interest = total-P
            monthly_var.set(f"{round(monthly,2):,.2f} €")
            total_var.set(f"{round(total,2):,.2f} €")
            interest_var.set(f"{round(interest,2):,.2f} €")
        except:
            monthly_var.set("Error"); total_var.set("—"); interest_var.set("—")

    accent_button(frame, "Calculate", calc_loan)

    results = tk.Frame(frame, bg=BG3)
    results.pack(fill="x")
    for label, var, color in [("Monthly payment:", monthly_var, FG),
                               ("Total amount:", total_var, ACCENT),
                               ("Total interest:", interest_var, "#ff453a")]:
        row = tk.Frame(results, bg=BG3)
        row.pack(fill="x", padx=12, pady=6)
        tk.Label(row, text=label, bg=BG3, fg=FG_DIM,
                 font=("Helvetica", 12)).pack(side="left")
        tk.Label(row, textvariable=var, bg=BG3, fg=color,
                 font=("Helvetica", 16, "bold")).pack(side="right")

# ─── MAIN WINDOW ────────────────────────────────────
root = tk.Tk()
root.title("Calculator v3.0")
root.configure(bg=BG)
root.resizable(False, False)
root.geometry("480x700")

tab_bar = tk.Frame(root, bg="#111113")
tab_bar.pack(fill="x")
tk.Frame(root, bg="#333", height=1).pack(fill="x")

content = tk.Frame(root, bg=BG2)
content.pack(fill="both", expand=True)

tabs_config = [
    ("🧮", "Basic",      build_calculator, "#ff9f0a"),
    ("📐", "Converter",  build_converter,  "#30d158"),
    ("📊", "Percentage", build_percentage, "#5ac8fa"),
    ("💪", "Fitness",    build_fitness,    "#bf5af2"),
    ("🏦", "Loan",       build_loan,       "#ff453a"),
]

tab_contents   = []
tab_btns       = []
tab_indicators = []
active_tab     = tk.IntVar(value=0)

def switch_tab(i):
    active_tab.set(i)
    for j, c in enumerate(tab_contents):
        c.pack(fill="both", expand=True) if j==i else c.pack_forget()
    for j, (btn, ind) in enumerate(zip(tab_btns, tab_indicators)):
        _, _, _, color = tabs_config[j]
        if j==i:
            btn.config(fg=color, font=("Helvetica", 9, "bold"),
                       bg=BG2, activebackground=BG2, activeforeground=color)
            ind.config(bg=color)
        else:
            btn.config(fg=FG_DIM, font=("Helvetica", 9),
                       bg="#111113", activebackground="#111113", activeforeground=FG_DIM)
            ind.config(bg="#111113")

for i, (icon, name, builder, color) in enumerate(tabs_config):
    col = tk.Frame(tab_bar, bg="#111113")
    col.pack(side="left", expand=True, fill="x")
    btn = tk.Button(col, text=f"{icon}\n{name}", font=("Helvetica", 9),
                    bg="#111113", fg=FG_DIM, relief="flat", bd=0,
                    cursor="hand2", pady=8,
                    activebackground="#111113", activeforeground=color,
                    command=lambda x=i: switch_tab(x))
    btn.pack(fill="x")
    btn.bind("<Enter>", lambda e, b=btn, x=i, c=color:
             b.config(fg=c) if active_tab.get()!=x else None)
    btn.bind("<Leave>", lambda e, b=btn, x=i:
             b.config(fg=FG_DIM) if active_tab.get()!=x else None)
    tab_btns.append(btn)
    ind = tk.Frame(col, bg="#111113", height=2)
    ind.pack(fill="x")
    tab_indicators.append(ind)
    c = tk.Frame(content, bg=BG2)
    tab_contents.append(c)
    builder(c)

switch_tab(0)
root.mainloop()