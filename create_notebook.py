import json

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Particle in a 1-D Box\n",
            "\n",
            "# Please Enter your Name, Roll No, Section below:\n",
            "\n",
            "Roshni Rakshit 103850 B.Tech\n",
            "\n",
            "## Motivation\n",
            "\n",
            "To demonstrate how to use the Schrodinger equation we will look at one of the simplest quantum problems: particle in a box. This problem simply asks what are the solutions to the Shrodinger equation for a particle that is allowed to travel in one dimension in a finite domain.\n",
            "\n",
            "## Learning Goals\n",
            "\n",
            "After working through these notes, you will be able to:\n",
            "1. Solve the Schrodinger equation for a 1D particle in a finite box\n",
            "2. Plot 1D particle in a box wave functions.\n",
            "\n",
            "## Coding Concepts\n",
            "\n",
            "The following coding concepts are used in this notebook:\n",
            "1. Variables\n",
            "2. Functions\n",
            "3. Plotting with matplotlib\n",
            "\n",
            "## Particle in a Box: Setting up the Problem\n",
            "\n",
            "To see the utility of the Schrodinger equation we will see what it predicts for the energy of a particle that can travel in one dimension but is restricted to a finite domain.\n",
            "\n",
            "$$\\hat{H}\\psi(x) = E\\psi(x)$$\n",
            "\n",
            "$$-\\frac{\\hbar^2}{2m}\\frac{d^2}{dx^2}\\psi(x) = E\\psi(x) \\quad 0\\leq x\\leq a$$\n",
            "\n",
            "And the energy eigenvalues are given by:\n",
            "$$E_n = \\frac{n^2 \\hbar^2 \\pi^2}{2 m a^2}$$\n",
            "\n",
            "Normalized wave functions:\n",
            "$$\\psi_n(x) = \\sqrt{\\frac{2}{a}} \\sin\\left(\\frac{n\\pi x}{a}\\right)$$"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import scipy.constants as const\n",
            "\n",
            "def psi(x, n, a):\n",
            "    return np.sqrt(2 / a) * np.sin(n * np.pi * x / a)\n",
            "\n",
            "h_bar = const.hbar\n",
            "m_e = const.m_e\n",
            "j_to_ev = const.e\n",
            "\n",
            "def calculate_energy_ev(n, a_nm):\n",
            "    a_m = a_nm * 1e-9\n",
            "    energy_joules = (n**2 * h_bar**2 * np.pi**2) / (2 * m_e * a_m**2)\n",
            "    energy_ev = energy_joules / j_to_ev\n",
            "    return energy_ev\n",
            "\n",
            "x = np.arange(0, 1, 0.001)\n",
            "a = 1\n",
            "n = 1"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig = plt.figure(figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')\n",
            "ax = plt.subplot(111)\n",
            "ax.grid(which='major', axis='both', color='#808080', linestyle='--')\n",
            "ax.set_xlabel(r'$x/a$', size=20)\n",
            "ax.set_ylabel(r'$\\psi(x)$', size=20)\n",
            "plt.tick_params(axis='both', labelsize=20)\n",
            "ax.plot(x, psi(x, n, a), label=n, lw=2)\n",
            "plt.title(\"Wavefunctions of Particle in a Box\", fontsize=20)\n",
            "ax.legend(fontsize=12, markerscale=5.0)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Exercise 1: Energy Level Pattern Recognition\n",
            "Run the energy-level calculation for **L = 1 nm** and fill the table:\n",
            "\n",
            "| n | Energy (eV) | Spacing vs previous |\n",
            "|---|-------------|---------------------|\n",
            "| 1 | 0.3760 | – |\n",
            "| 2 | 1.5041 | Larger |\n",
            "| 3 | 3.3843 | Larger |\n",
            "| 4 | 6.0165 | Larger |\n",
            "| 5 | 9.4008 | Larger |\n",
            "\n",
            "**Question:** As *n* increases, spacing between levels:\n",
            "- [x] Increases\n",
            "- [ ] Decreases\n",
            "- [ ] Remains constant"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "a = 1\n",
            "for n_val in range(1, 6):\n",
            "    energy = calculate_energy_ev(n=n_val, a_nm=a)\n",
            "    print(f\"n = {n_val}, Energy = {energy:.4f} eV\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Exercise 1: Manual Entry Table\n",
            "\n",
            "| n | Energy (eV) | Spacing vs previous |\n",
            "|---|-------------|---------------------|\n",
            "| 1 | 0.3760 | – |\n",
            "| 2 | 1.5041 | 1.1281 eV (Larger) |\n",
            "| 3 | 3.3843 | 1.8802 eV (Larger) |\n",
            "| 4 | 6.0165 | 2.6322 eV (Larger) |\n",
            "| 5 | 9.4008 | 3.3843 eV (Larger) |"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Exercise 2: Box Length vs Energy (What-if)\n",
            "Change **L = 1 nm → 2 nm → 5 nm** and record **E₁**:\n",
            "\n",
            "| L (nm) | E₁ (eV) |\n",
            "|-------:|--------:|\n",
            "| 1 | 0.3760 |\n",
            "| 2 | 0.0940 |\n",
            "| 5 | 0.0150 |\n",
            "\n",
            "**Concept check:** Increasing L makes E₁:\n",
            "- [ ] Increase\n",
            "- [x] Decrease\n",
            "- [ ] Stay the same"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "n_val = 1\n",
            "for a_val in [1, 2, 3, 4, 5]:\n",
            "    energy = calculate_energy_ev(n=n_val, a_nm=a_val)\n",
            "    print(f\"L = {a_val}, Energy = {energy:.4f} eV\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Exercise 2: Manual Entry Table\n",
            "\n",
            "| L | Energy (eV) | Spacing vs previous |\n",
            "|---|-------------|---------------------|\n",
            "| 1 | 0.3760 | – |\n",
            "| 2 | 0.0940 | -0.2820 eV |\n",
            "| 3 | 0.0418 | -0.0522 eV |\n",
            "| 4 | 0.0235 | -0.0183 eV |\n",
            "| 5 | 0.0150 | -0.0085 eV |"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Exercise 3: Wavefunction Shape & Nodes\n",
            "Plot ψ(x) for **n = 1, 2, 3**.\n",
            "\n",
            "Fill:\n",
            "| n | Nodes inside the box |\n",
            "|---|----------------------|\n",
            "| 1 | 0 |\n",
            "| 2 | 1 |\n",
            "| 3 | 2 |\n",
            "\n",
            "Choose:\n",
            "- [ ] nodes = n\n",
            "- [x] nodes = n − 1\n",
            "- [ ] nodes = 2n"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "x = np.arange(0, 1, 0.001)\n",
            "a = 1\n",
            "\n",
            "fig = plt.figure(figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')\n",
            "ax = plt.subplot(111)\n",
            "ax.grid(which='major', axis='both', color='#808080', linestyle='--')\n",
            "ax.set_xlabel(r'$x/a$', size=20)\n",
            "ax.set_ylabel(r'$\\psi(x)$', size=20)\n",
            "plt.tick_params(axis='both', labelsize=20)\n",
            "\n",
            "for n_val in [1, 2, 3]:\n",
            "    ax.plot(x, psi(x, n_val, a), label=f'n = {n_val}', lw=2)\n",
            "\n",
            "plt.title(\"Wavefunctions of Particle in a Box\", fontsize=20)\n",
            "ax.legend(fontsize=12, markerscale=5.0)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Exercise 4: Probability Density Insight\n",
            "Plot $|\\psi_n(x)|^2$ for **n = 1** and **n = 3** and select correct statements:\n",
            "\n",
            "- [ ] Electron is equally likely everywhere  \n",
            "- [x] Electron is never found at the walls  \n",
            "- [x] Higher n leads to more oscillations  \n",
            "- [ ] Probability density can be negative"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def psi_squared(x, n, a):\n",
            "    return np.square(psi(x, n, a))\n",
            "\n",
            "x = np.arange(0, 1, 0.001)\n",
            "a = 1\n",
            "\n",
            "fig = plt.figure(figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')\n",
            "ax = plt.subplot(111)\n",
            "ax.grid(which='major', axis='both', color='#808080', linestyle='--')\n",
            "ax.set_xlabel(r'$x/a$', size=20)\n",
            "ax.set_ylabel(r'$\\psi^2(x)$', size=20)\n",
            "plt.tick_params(axis='both', labelsize=20)\n",
            "\n",
            "for n_val in [1, 3]:\n",
            "    ax.plot(x, psi_squared(x, n_val, a), label=f'n = {n_val}', lw=2)\n",
            "\n",
            "plt.title(\"Probability Density of Particle in a Box\", fontsize=20)\n",
            "ax.legend(fontsize=12, markerscale=5.0)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Exercise 5: Nano-Connection (2–3 lines)\n",
            "Pick ONE: Quantum dots / LEDs / Nanowires / Metal nanoparticles.\n",
            "\n",
            "Selected: **Quantum dots**\n",
            "\n",
            "**Prompt:** Why does reducing size change color/electrical behavior?\n",
            "\n",
            "When the physical size of a quantum dot is decreased, the spatial confinement dimension L becomes smaller, which increases the energy bandgap because energy scales as 1/L^2. Due to this larger energy separation, smaller quantum dots emit shorter wavelengths of light (blue shift), directly tuning the color and electronic band properties.\n",
            "\n",
            "---\n",
            "\n",
            "## Mini-Challenge (No math)\n",
            "If an electron is confined in a **very tiny box**, its energy will be:\n",
            "- [ ] Very small\n",
            "- [ ] Moderate\n",
            "- [x] Very large\n",
            "\n",
            "**Explain in one sentence:**\n",
            "Confining the electron to an extremely tiny region restricts its position and drastically increases its momentum and kinetic energy according to the Heisenberg uncertainty principle."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## MCQ Quiz (Auto-graded, single attempt)\n",
            "\n",
            "**Answers Summary:**\n",
            "1. E ∝ n^2\n",
            "2. Decreases\n",
            "3. n − 1\n",
            "4. Is always ≥ 0\n",
            "5. Discrete energies in nanoscale structures"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import json\n",
            "import os\n",
            "import datetime\n",
            "\n",
            "QUESTIONS = [\n",
            "    {\n",
            "        \"q\": \"1) In a 1D particle-in-a-box, energy levels scale with quantum number n as:\",\n",
            "        \"options\": [\"E ∝ n\", \"E ∝ n^2\", \"E ∝ 1/n\", \"E is constant for all n\"],\n",
            "        \"answer\": 1\n",
            "    },\n",
            "    {\n",
            "        \"q\": \"2) If the box length L increases, the energy spacing between levels:\",\n",
            "        \"options\": [\"Increases\", \"Decreases\", \"Stays the same\", \"Becomes random\"],\n",
            "        \"answer\": 1\n",
            "    },\n",
            "    {\n",
            "        \"q\": \"3) The number of nodes (zero crossings inside the box) in ψ_n(x) is:\",\n",
            "        \"options\": [\"n\", \"n − 1\", \"2n\", \"Always 0\"],\n",
            "        \"answer\": 1\n",
            "    },\n",
            "    {\n",
            "        \"q\": \"4) The probability density |ψ(x)|^2:\",\n",
            "        \"options\": [\"Can be negative\", \"Is always ≥ 0\", \"Is always constant\", \"Is undefined at the walls\"],\n",
            "        \"answer\": 1\n",
            "    },\n",
            "    {\n",
            "        \"q\": \"5) Quantum confinement is most directly related to:\",\n",
            "        \"options\": [\"Bigger objects having bigger mass\", \"Energy becoming continuous\", \"Discrete energies in nanoscale structures\", \"Classical friction in materials\"],\n",
            "        \"answer\": 2\n",
            "    },\n",
            "]\n",
            "\n",
            "SUBMISSION_FILE = \"mcq_submission.json\"\n",
            "def already_submitted(): return os.path.exists(SUBMISSION_FILE)\n",
            "def load_submission():\n",
            "    with open(SUBMISSION_FILE, \"r\") as f: return json.load(f)\n",
            "def save_submission(payload):\n",
            "    with open(SUBMISSION_FILE, \"w\") as f: json.dump(payload, f, indent=2)\n",
            "\n",
            "try:\n",
            "    import ipywidgets as widgets\n",
            "    from IPython.display import display, Markdown, clear_output\n",
            "except Exception:\n",
            "    widgets = None\n",
            "\n",
            "if already_submitted():\n",
            "    sub = load_submission()\n",
            "    print(f\"Quiz already submitted. Score: {sub.get('score')}/{sub.get('total')}\")\n",
            "else:\n",
            "    radios = []\n",
            "    for item in QUESTIONS:\n",
            "        r = widgets.RadioButtons(options=item[\"options\"], value=None, layout={\"width\": \"max-content\"})\n",
            "        radios.append(r)\n",
            "\n",
            "    submit_btn = widgets.Button(description=\"Submit Answer\", button_style=\"danger\")\n",
            "    out = widgets.Output()\n",
            "\n",
            "    def on_submit(_):\n",
            "        if any(r.value is None for r in radios):\n",
            "            with out:\n",
            "                clear_output()\n",
            "                print(\"Please answer all questions.\")\n",
            "            return\n",
            "\n",
            "        selected = [QUESTIONS[i][\"options\"].index(r.value) for i, r in enumerate(radios)]\n",
            "        score = sum(1 for i, v in enumerate(selected) if v == QUESTIONS[i][\"answer\"])\n",
            "        payload = {\"submitted_at\": str(datetime.datetime.now()), \"selected\": selected, \"score\": score, \"total\": len(QUESTIONS)}\n",
            "        save_submission(payload)\n",
            "        for r in radios:\n",
            "            r.disabled = True\n",
            "        submit_btn.disabled = True\n",
            "        with out:\n",
            "            clear_output()\n",
            "            print(f\"Submitted! Score: {score}/{len(QUESTIONS)}\")\n",
            "\n",
            "    submit_btn.on_click(on_submit)\n",
            "    display(Markdown(\"### Particle in a Box Quiz\"))\n",
            "    for i, item in enumerate(QUESTIONS):\n",
            "        display(Markdown(f\"**{item['q']}**\"))\n",
            "        display(radios[i])\n",
            "    display(submit_btn, out)"
        ]
    }
]

nb = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("Particle_in_a_1D_Box.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Particle_in_a_1D_Box.ipynb created successfully.")
