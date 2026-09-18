"""Fill the PRC-I review template with the Network Logs Anomaly Detection project.

Reads PRC-extended.pptx (the department template with the extra slides this
review needs) from this script's directory and writes the filled deck to the
working directory. Re-running rebuilds from the template, so it is safe to run
repeatedly.
"""
import os
from copy import deepcopy

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Inches

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "PRC-extended.pptx")
DST = "Project_Network_Anomaly_Detection.pptx"

XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


# ----------------------------------------------------------------- helpers
def body_paragraphs(tf):
    return tf._txBody.findall(qn("a:p"))


def prototype(tf, index=0):
    """A copy of one paragraph, trimmed to a single run, used as a stencil."""
    paras = [p for p in body_paragraphs(tf) if p.findall(qn("a:r"))]
    proto = deepcopy(paras[min(index, len(paras) - 1)])
    runs = proto.findall(qn("a:r"))
    for extra in runs[1:]:
        proto.remove(extra)
    for br in proto.findall(qn("a:br")):
        proto.remove(br)
    return proto


def write_paragraphs(tf, items, proto_index=0, size=None):
    """Replace a text frame's paragraphs, keeping the template's own styling.

    items is a sequence of (text, level) or (text, level, bold) tuples.
    """
    proto = prototype(tf, proto_index)
    body = tf._txBody
    for p in body_paragraphs(tf):
        body.remove(p)
    for item in items:
        text, level = item[0], item[1]
        bold = item[2] if len(item) > 2 else False
        para = deepcopy(proto)
        pPr = para.find(qn("a:pPr"))
        if pPr is None:
            pPr = para.makeelement(qn("a:pPr"), {})
            para.insert(0, pPr)
        if level:
            pPr.set("lvl", str(level))
        else:
            pPr.attrib.pop("lvl", None)
        run = para.find(qn("a:r"))
        if bold or size:
            rPr = run.find(qn("a:rPr"))
            if rPr is None:
                rPr = run.makeelement(qn("a:rPr"), {})
                run.insert(0, rPr)
            if bold:
                rPr.set("b", "1")
            if size:
                rPr.set("sz", str(int(size * 100)))
        t = run.find(qn("a:t"))
        t.text = text
        t.set(XML_SPACE, "preserve")
        body.append(para)


def set_paragraph_text(tf, index, text):
    """Rewrite one paragraph in place, preserving its run formatting."""
    para = body_paragraphs(tf)[index]
    runs = para.findall(qn("a:r"))
    for extra in runs[1:]:
        para.remove(extra)
    t = runs[0].find(qn("a:t"))
    t.text = text
    t.set(XML_SPACE, "preserve")


def replace_run_text(tf, needle, replacement):
    """Swap the text of the single run carrying `needle`, leaving the
    surrounding runs and line breaks of that paragraph intact."""
    for para in body_paragraphs(tf):
        for run in para.findall(qn("a:r")):
            t = run.find(qn("a:t"))
            if t is not None and t.text and needle in t.text:
                t.text = t.text.replace(needle, replacement)
                t.set(XML_SPACE, "preserve")
                return True
    raise KeyError("run containing %r not found" % needle)


def shape_by_name(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise KeyError("%s not on slide" % name)


def first_table(slide):
    for sh in slide.shapes:
        if sh.has_table:
            return sh.table
    raise KeyError("no table on slide")


def table_frame(slide):
    for sh in slide.shapes:
        if sh.has_table:
            return sh
    raise KeyError("no table on slide")


def set_cell(cell, text, size=None):
    tf = cell.text_frame
    paras = body_paragraphs(tf)
    para = paras[0]
    runs = para.findall(qn("a:r"))
    for extra in paras[1:]:
        tf._txBody.remove(extra)
    if not runs:
        # An empty cell carries no run to copy formatting from. Build one, and
        # place it before a:endParaRPr - PowerPoint ignores runs that follow it.
        run = para.makeelement(qn("a:r"), {})
        end_rPr = para.find(qn("a:endParaRPr"))
        if end_rPr is not None:
            new_rPr = deepcopy(end_rPr)
            new_rPr.tag = qn("a:rPr")
            run.append(new_rPr)
        t = run.makeelement(qn("a:t"), {})
        run.append(t)
        if end_rPr is not None:
            end_rPr.addprevious(run)
        else:
            para.append(run)
        runs = [run]
    for extra in runs[1:]:
        para.remove(extra)
    run = runs[0]
    if size:
        rPr = run.find(qn("a:rPr"))
        if rPr is None:
            rPr = run.makeelement(qn("a:rPr"), {})
            run.insert(0, rPr)
        rPr.set("sz", str(int(size * 100)))
    t = run.find(qn("a:t"))
    t.text = text
    t.set(XML_SPACE, "preserve")


def add_table_rows(table, count):
    tbl = table._tbl
    template_row = tbl.findall(qn("a:tr"))[-1]
    for _ in range(count):
        tbl.append(deepcopy(template_row))


def trim_table_rows(table, keep):
    tbl = table._tbl
    for extra in tbl.findall(qn("a:tr"))[keep:]:
        tbl.remove(extra)


# -------------------------------------------------------------------- fill
pres = Presentation(SRC)
slides = list(pres.slides)

# --- 1: title ------------------------------------------------------------
replace_run_text(
    shape_by_name(slides[0], "Title 1").text_frame,
    "Project Title",
    "Network Logs Anomaly Detection",
)
set_paragraph_text(
    shape_by_name(slides[0], "Content Placeholder 2").text_frame,
    1,
    "2320030085\t\tVirinchi Deevi",
)

# --- 2: outline ----------------------------------------------------------
write_paragraphs(
    shape_by_name(slides[1], "Content Placeholder 8").text_frame,
    [
        ("Introduction", 0),
        ("Problem Statement", 0),
        ("Objectives", 0),
        ("Literature Survey", 0),
        ("Research Gap Identification", 0),
        ("Innovation, Creativity, and Novelty", 0),
        ("Methodology", 0),
        ("System Design and Architecture", 0),
        ("Use of Modern Tools and Technologies", 0),
        ("Implementation, Coding Quality, and Functionality", 0),
        ("Experimental Setup and Preliminary Results", 0),
        ("Feasibility and Project Plan", 0),
        ("Research Paper Draft Preparation", 0),
        ("Conclusion", 0),
        ("References", 0),
    ],
    size=20,
)

# Fifteen entries do not fit one column at a readable size.
outline_bodyPr = shape_by_name(
    slides[1], "Content Placeholder 8"
).text_frame._txBody.find(qn("a:bodyPr"))
outline_bodyPr.set("numCol", "2")
outline_bodyPr.set("spcCol", "457200")  # half-inch gutter

# --- 3: introduction -----------------------------------------------------
write_paragraphs(
    shape_by_name(slides[2], "Content Placeholder 8").text_frame,
    [
        ("Background", 0, True),
        (
            "Every connection a network makes is recorded as a log line: source and "
            "destination address, port, protocol, bytes transferred and duration.",
            1,
        ),
        ("Importance", 0, True),
        (
            "An intrusion is present in those logs, but only as a pattern across many "
            "records. A single connection to port 22 is routine; forty of them in four "
            "minutes is an attack. The volume makes manual review impossible.",
            1,
        ),
        ("Problem being solved", 0, True),
        (
            "Detecting port scanning, denial of service, brute force and data "
            "exfiltration in network connection logs, with every alert traceable to the "
            "rule and threshold that raised it.",
            1,
        ),
        ("Application", 0, True),
        (
            "Security monitoring for small and medium internal networks, and an "
            "explainable baseline against which learning-based detectors can be compared.",
            1,
        ),
    ],
)

# --- 4: problem statement ------------------------------------------------
write_paragraphs(
    shape_by_name(slides[3], "Content Placeholder 2").text_frame,
    [
        (
            "Network connection logs accumulate faster than any analyst can read them, "
            "and an intrusion is not visible in a single record. It is a property of a "
            "group of connections inside a time window.",
            0,
        ),
        (
            "Detectors that measure those windows against the system clock return "
            "different results depending on the hour of execution and the timezone of "
            "the host, which makes them impossible to evaluate, tune or trust.",
            0,
        ),
        (
            "This project detects attack patterns in network connection logs such that "
            "the result depends only on the data, and every detection can be explained "
            "to the person acting on it.",
            0,
        ),
    ],
)

# --- 5: objectives -------------------------------------------------------
write_paragraphs(
    shape_by_name(slides[4], "Content Placeholder 8").text_frame,
    [
        (
            "Build an ETL pipeline that ingests network connection logs, normalises "
            "them and stores them in an indexed relational database.",
            0,
        ),
        (
            "Implement six rule-based detectors covering port scanning, denial of "
            "service, brute force, data exfiltration, dangerous ports and hostile "
            "address ranges.",
            0,
        ),
        (
            "Anchor every detection window on log time rather than system time, so that "
            "output is identical across runs, hosts and timezones.",
            0,
        ),
        (
            "Attribute every detection to a rule, a severity level and a description an "
            "analyst can act on.",
            0,
        ),
        (
            "Present the results in an interactive dashboard that reads the same store "
            "the detector writes, so display cannot disagree with detection.",
            0,
        ),
        (
            "Verify determinism, idempotency and reproducibility by measurement rather "
            "than assumption.",
            0,
        ),
    ],
)

# --- 6-8: literature survey ----------------------------------------------
# Twelve columns across one slide leave roughly an inch each, so every cell is
# written short and the seventeen papers are split over three slides.
PAPERS = [
    ("2025", "Goldschmidt & Chuda",
     "Network Intrusion Datasets: Survey, Limitations, Recommendations",
     "Computers & Security",
     "Review public NIDS datasets and their suitability",
     "Systematic review; 13-property comparison", "89 public datasets",
     "Dataset properties; usage in current research",
     "Data scarcity is the main obstacle; recent datasets go unused",
     "No agreed practice for dataset selection and reporting",
     "10.1016/j.cose.2025.104510"),
    ("2022", "Holland, Schmitt, Mittal & Feamster",
     "Towards Reproducible Network Traffic Analysis", "arXiv",
     "Explain why traffic analysis results cannot be compared",
     "pcapML: metadata embedded in captures", "Public traffic datasets",
     "Dataset interpretation; pipeline reproducibility",
     "Inconsistent interpretation prevents judging real advances",
     "No standard dataset format",
     "10.48550/arXiv.2203.12410"),
    ("2024", "Moulton, McCully & Hastings",
     "Confronting the Reproducibility Crisis in Cybersecurity AI",
     "IEEE CARS", "Document barriers to reproducing published results",
     "Case study using the VeriGauge toolkit", "Prior published experiments",
     "Dependencies; hardware; versioning",
     "Version conflict and obsolescence defeat reproduction",
     "No protocol for long-term reproducibility",
     "10.1109/CARS61786.2024.10778911"),
    ("2023", "Lamberts, Wolsing, Wagner et al.",
     "SoK: Evaluations in Industrial Intrusion Detection Research",
     "Journal of Systems Research",
     "Analyse how intrusion detection research evaluates itself",
     "Systematic analysis of publications", "609 publications",
     "Datasets per paper; metric choice",
     "1.3 datasets per paper on average; metrics stay ambiguous",
     "Fragmented evaluation hides real progress",
     "10.5070/SR33162445"),
    ("2025", "Wang, Zheng, Gui, Hua & Hassan",
     "Are We There Yet? Graph Network Intrusion Detection Systems",
     "arXiv", "Reproduce published graph NIDS results",
     "Re-evaluation under adversarial attack",
     "3 public datasets and 1 enterprise",
     "False positive rate; robustness",
     "Large performance discrepancies appear on reproduction",
     "Replication studies are absent from the field",
     "10.48550/arXiv.2503.20281"),
    ("2025", "Verkerken, D'hooge, Volckaert et al.",
     "ConCap: Practical Network Traffic Generation for IDS",
     "IEEE SaTML", "Generate realistic labelled traffic reproducibly",
     "Containerised scenarios from config files",
     "10 activities; 21 variants",
     "Flow equivalence to real traffic; reproducibility",
     "Generated flows match real traffic for detection purposes",
     "Prior studies rest on unobtainable training data",
     "10.1109/SaTML68715.2026.00051"),
    ("2025", "Mohale & Obagbuwa",
     "Systematic Review of Explainable AI in Intrusion Detection",
     "Frontiers in AI", "Review XAI for the IDS black-box problem",
     "SHAP; LIME; decision trees; hybrids",
     "CICIDS2017; KDD Cup 99",
     "Accuracy; false positives; interpretability; cost",
     "Overhead and the accuracy trade-off block real-time XAI",
     "No standard interpretability metric",
     "10.3389/frai.2025.1526221"),
    ("2024", "Kumar & Thing",
     "Evaluating the Explainability of Deep Learning NIDS", "arXiv",
     "Assess whether DL NIDS decisions can be explained",
     "XAI tools; global and local agreement criteria",
     "Several attack datasets",
     "Explainability per model; agreement between tools",
     "XAI tools disagree with each other on most models",
     "Prior work ignored state-of-the-art DL NIDS",
     "10.48550/arXiv.2408.14040"),
    ("2023", "Wei, Jang-Jaccard, Singh et al.",
     "DDoS Attack Detection and Explanation using SHAP", "arXiv",
     "Classify DDoS traffic and explain the classification",
     "XGBoost SHAP selection; MLP classifier", "DDoS attack dataset",
     "Feature importance; accuracy",
     "Above 99% accuracy on 20 selected features",
     "Interpretability asserted but not standardised",
     "10.48550/arXiv.2306.17190"),
    ("2025", "Teuwen, Mulders, Zambon & Allodi",
     "Ruling the Unruly: Low-Noise Intrusion Detection Rules", "ACM",
     "Identify what makes a signature-based rule good",
     "Empirical study; interviews with rule designers",
     "Rules and alerts from a commercial SOC",
     "Rule specificity; analyst workload; coverage",
     "Six design principles; generalised rules raise coverage and workload",
     "Coverage versus analyst workload unresolved",
     "10.1145/3708821.3710823"),
    ("2023", "Alharbi & Khan",
     "Ensemble Defense System: A Hybrid IDS Approach", "IEEE ITNAC",
     "Combine signature and anomaly detection in one framework",
     "Suricata; Zeek; Slips; Elasticsearch",
     "Scripted port scan, privilege escalation, DoS",
     "Detection across attack categories",
     "The hybrid framework detected every tested attack category",
     "No evaluation of alert volume at scale",
     "10.1109/ITNAC59571.2023.10368510"),
    ("2025", "Miguel-Diez, Campazas-Vega et al.",
     "Anomaly Detection in Network Flows using Unsupervised Online ML",
     "arXiv", "Detect anomalies without labelled training data",
     "Online One-Class SVM (River library)",
     "NF-UNSW-NB15 and v2",
     "Accuracy >98%; false positives <3.1%; 0.033 ms per flow",
     "Online unsupervised detection is fast enough for real time",
     "Generalisation across networks not established",
     "10.48550/arXiv.2509.01375"),
    ("2024", "Talukder, Islam, Uddin et al.",
     "ML Network Intrusion Detection for Big and Imbalanced Data",
     "Journal of Big Data",
     "Handle class imbalance in large intrusion datasets",
     "Oversampling; stacking embedding; PCA; DT/RF/ET",
     "UNSW-NB15; CIC-IDS2017; CIC-IDS2018",
     "Accuracy per dataset and classifier",
     "Accuracy of 99.59-99.99% reported across three datasets",
     "Near-perfect accuracy invites leakage questions",
     "10.48550/arXiv.2401.12262"),
    ("2024", "Vitorino, Silva, Maia & Praca",
     "An Adversarial Robustness Benchmark for Enterprise NIDS",
     "FPS 2023", "Compare model robustness under standard conditions",
     "RF; XGBoost; LightGBM; EBM; adversarial training",
     "CICIDS2017; NewCICIDS; HIKARI",
     "Robustness; false alarm rate; generalisation",
     "The corrected dataset improved results; adversarial training helped",
     "Transferability across environments untested",
     "10.1007/978-3-031-57537-2_1"),
    ("2025", "Xu, Wu, Wang, Gao et al.",
     "Deep Learning-based Intrusion Detection Systems: A Survey",
     "arXiv", "Survey the full deep-learning IDS pipeline",
     "Review across six pipeline stages",
     "Public DL-IDS benchmarks",
     "Generalisation; zero-day detection",
     "Deep learning generalises beyond signature matching",
     "Pipeline stages are studied in isolation",
     "10.48550/arXiv.2504.07839"),
    ("2025", "Feng & Sakurai",
     "NIDS: From Conventional Approaches to LLM Collaboration",
     "arXiv", "Trace NIDS from signatures through neural nets to LLMs",
     "Literature review across network, vehicular and IoT settings",
     "Datasets of the reviewed studies",
     "Signature effectiveness; LLM benefit and risk",
     "Signature methods retain value; neural detection still hard to deploy",
     "LLM deployment and LLM-enabled attacks are open",
     "10.48550/arXiv.2510.23313"),
    ("2025", "Jamshidi, Nafi, Nikanjam & Khomh",
     "Evaluating ML-Driven IDS in IoT: Performance and Energy",
     "Computers & Industrial Engineering",
     "Measure the cost of running ML IDS at the network edge",
     "Empirical comparison of ML and DL IDS; ANOVA",
     "Edge deployment, benign and attack",
     "CPU load; CPU usage; energy consumption",
     "Edge IDS raise resource consumption sharply during attacks",
     "Little work measures IDS cost under real-time threat",
     "10.1016/j.cie.2025.111103"),
]

LIT_SLIDES = (5, 6, 7)
PER_SLIDE = 6
COL_WIDTHS = [0.35, 0.44, 0.96, 1.39, 0.87, 1.13, 1.13, 0.87, 0.87, 1.13, 1.13, 1.22]
HEADINGS = ["Sl No", "Year", "Authors", "Title of the paper", "Source",
            "Objective", "Techniques Used", "Dataset Used",
            "Parameters Analysed", "Research Inference", "Research Gap", "DOI"]
CELL_PT = 8

for n, slide_index in enumerate(LIT_SLIDES):
    slide = slides[slide_index]
    chunk = PAPERS[n * PER_SLIDE:(n + 1) * PER_SLIDE]

    write_paragraphs(
        shape_by_name(slide, "Title 7").text_frame,
        [("Literature Survey (%d of %d)" % (n + 1, len(LIT_SLIDES)), 0)],
    )
    write_paragraphs(
        shape_by_name(slide, "Content Placeholder 8").text_frame,
        [
            (
                "Seventeen papers published from 2022 onwards on rule-based and "
                "learning-based intrusion detection, benchmark datasets, and the "
                "reproducibility problems reported for network anomaly detection.",
                0,
            )
        ],
        size=14,
    )

    frame = table_frame(slide)
    frame.left, frame.top = Inches(0.92), Inches(2.05)
    frame.width, frame.height = Inches(11.5), Inches(4.7)

    table = first_table(slide)
    needed = 1 + len(chunk)
    if len(table.rows) < needed:
        add_table_rows(table, needed - len(table.rows))
    trim_table_rows(table, needed)

    for i, width in enumerate(COL_WIDTHS):
        table.columns[i].width = Inches(width)
    # The template's rows are short; give them room so the filled table uses
    # the space between the intro line and the footer.
    for i, row in enumerate(table.rows):
        row.height = Inches(0.34) if i == 0 else Inches(0.62)

    for c, head in enumerate(HEADINGS):
        set_cell(table.rows[0].cells[c], head, size=CELL_PT)

    for r, paper in enumerate(chunk, start=1):
        values = [str(n * PER_SLIDE + r)] + list(paper)
        for c, text in enumerate(values):
            set_cell(table.rows[r].cells[c], text, size=CELL_PT)

# --- 9: research gap -----------------------------------------------------
write_paragraphs(
    shape_by_name(slides[8], "Content Placeholder 8").text_frame,
    [
        (
            "Gaps addressed: detection windows measured against the system clock make "
            "results irreproducible; learning-based alerts carry no reason an analyst "
            "can act on; traffic without realistic attack bursts hides what is "
            "detectable.",
            0,
        ),
    ],
)

# Cells stay short: the template's columns are narrow, and a long string wraps
# into a row tall enough to push later rows off the slide.
gap_rows = [
    [
        "1",
        "Towards Reproducible Network Traffic Analysis",
        "Holland et al.",
        "pcapML; standardised capture metadata",
        "Inconsistent dataset interpretation blocks comparison",
        "No standard format, so results cannot be compared",
    ],
    [
        "2",
        "SoK: Evaluations in Industrial IDS Research",
        "Lamberts et al.",
        "Systematic analysis of 609 papers",
        "1.3 datasets per paper; metrics ambiguous",
        "Fragmented evaluation hides real progress",
    ],
    [
        "3",
        "Ruling the Unruly: Low-Noise IDS Rules",
        "Teuwen et al.",
        "Empirical study of deployed SOC rules",
        "Generalised rules raise coverage and workload together",
        "Rule quality is undefined without stated thresholds",
    ],
]

gap_table = first_table(slides[8])
needed = 1 + len(gap_rows)
if len(gap_table.rows) < needed:
    add_table_rows(gap_table, needed - len(gap_table.rows))
for r, values in enumerate(gap_rows, start=1):
    for c, text in enumerate(values):
        set_cell(gap_table.rows[r].cells[c], text)
trim_table_rows(gap_table, needed)

# Filled rows are taller than the template's empty ones. Widen the table, give
# each column a width matched to its content, and lift it clear of the footer.
gap_frame = table_frame(slides[8])
gap_frame.left, gap_frame.top = Inches(0.92), Inches(2.85)
gap_frame.width = Inches(11.5)
for i, width in enumerate([0.5, 2.5, 1.7, 2.6, 2.1, 2.1]):
    gap_table.columns[i].width = Inches(width)
for row in gap_table.rows:
    row.height = Inches(0.4)

# --- 10: innovation, creativity, novelty ---------------------------------
tf = shape_by_name(slides[9], "TextBox 3").text_frame
set_paragraph_text(
    tf, 1,
    "Detection windows are anchored on the timestamp of the record being examined "
    "rather than on the system clock, so the same input produces the same output on "
    "any machine, in any timezone, at any hour.",
)
set_paragraph_text(
    tf, 4,
    "The dataset generator emits attacks as timed campaigns rather than scattered "
    "records, because density in time is the signal the detectors rely on. A seed "
    "reproduces the dataset byte for byte, so any result can be re-derived.",
)
set_paragraph_text(
    tf, 7,
    "Every alert carries the rule, threshold and description that produced it, "
    "addressing the explainability gap left by learning-based detectors. "
    "Determinism, idempotency and reproducibility are verified by measurement.",
)


# --- 11-15, 17: sections added for this review ---------------------------
def fill_section(index, heading, items):
    slide = slides[index]
    write_paragraphs(shape_by_name(slide, "Title 7").text_frame, [(heading, 0)])
    write_paragraphs(shape_by_name(slide, "Content Placeholder 8").text_frame, items)


fill_section(
    10,
    "Methodology",
    [
        ("Dataset design", 0, True),
        (
            "A week of traffic on a 192.168.1.0/24 network is modelled, with attacks "
            "emitted as timed campaigns rather than isolated records, because density "
            "in time is what a detector can recognise.",
            1,
        ),
        ("Extract, transform, load", 0, True),
        (
            "Timestamps are normalised to a single stored format, records are inserted "
            "into SQLite, and five indexes are built over time, source and destination.",
            1,
        ),
        ("Detection", 0, True),
        (
            "Each record is evaluated against the traffic that preceded it, inside a "
            "window that ends at that record's own timestamp. Six rules are applied in "
            "a fixed order and the first match assigns type, severity and description.",
            1,
        ),
        ("Verification", 0, True),
        (
            "Determinism is measured across independent runs, idempotency by "
            "re-execution over a scanned database, and reproducibility from a fixed seed.",
            1,
        ),
    ],
)

fill_section(
    11,
    "System Design and Architecture",
    [
        ("Four layers, one direction of flow", 0, True),
        (
            "Generation - log_generator.py produces 5,000 records, of which 275 belong "
            "to five labelled attack campaigns.",
            1,
        ),
        (
            "Storage - database.py normalises timestamps and loads records into SQLite; "
            "five indexes cover time, source, destination and destination-port lookups.",
            1,
        ),
        (
            "Detection - anomaly_detector.py applies six rules per record and writes "
            "each match to an anomalies table keyed to the originating log id.",
            1,
        ),
        ("Presentation - dashboard.py reads both tables and renders five views.", 1),
        ("Design decisions", 0, True),
        (
            "Detections are stored rather than recomputed, so the dashboard cannot "
            "disagree with the detector. Every window and threshold is a method "
            "argument, not a constant buried in a query.",
            1,
        ),
    ],
)

fill_section(
    12,
    "Use of Modern Tools and Technologies",
    [
        ("Python 3.14 - pipeline, detection rules and verification scripts", 0),
        ("SQLite 3.50 - embedded relational storage with indexed time-window queries", 0),
        ("pandas 3.0 - record handling and aggregation", 0),
        ("Streamlit 1.64 - interactive dashboard served on localhost", 0),
        ("Plotly 7.1 - six native interactive charts", 0),
        ("Git - version control, as required by the capstone policy", 0),
        ("Why these", 0, True),
        (
            "Every dependency is open source and installs without a server, so the "
            "system runs unchanged on any examiner's machine. Seeded generation and "
            "lower bounds in requirements.txt keep a demonstration repeatable.",
            1,
        ),
    ],
)

fill_section(
    13,
    "Implementation, Coding Quality, and Functionality",
    [
        ("Implementation", 0, True),
        (
            "Four modules, 869 lines of Python: log_generator.py (165), database.py "
            "(219), anomaly_detector.py (199) and dashboard.py (286).",
            1,
        ),
        ("Coding quality", 0, True),
        (
            "Every SQL statement is parameterised, so no address, port or threshold is "
            "interpolated into a query as a string. Each module carries docstrings, "
            "each rule is a separate method with its thresholds as named arguments, and "
            "paths resolve relative to the source file rather than the working directory.",
            1,
        ),
        ("Functionality", 0, True),
        (
            "Generation, load, detection and dashboard all run end to end from a clean "
            "checkout in 1.2 seconds. Detection is idempotent, so the pipeline can be "
            "re-run without corrupting counts.",
            1,
        ),
    ],
)

fill_section(
    14,
    "Experimental Setup and Preliminary Results",
    [
        ("Setup", 0, True),
        (
            "Windows 11, Python 3.14, SQLite 3.50. Dataset: 5,000 connection records "
            "spanning seven days, of which 275 belong to attack campaigns. Procedure: "
            "generate, load, detect and measure, repeated over three independent runs.",
            1,
        ),
        ("Results", 0, True),
        (
            "268 records flagged, a detection rate of 5.4%. By rule: brute force 79, "
            "suspicious IP 74, DDoS 61, port scan 30, uncommon port 13, exfiltration 11. "
            "By severity: 140 high, 104 medium, 13 low, 11 critical. Full pipeline "
            "runtime 1.2 seconds.",
            1,
        ),
        ("Verification", 0, True),
        (
            "Three independent runs returned 267, 267 and 268 detections; three rebuilds "
            "from one dataset returned 268 every time. Re-running the detector over a "
            "scanned database added nothing. A seeded dataset reproduced byte for byte.",
            1,
        ),
        ("Defect found and corrected", 0, True),
        (
            "Windows anchored on the system clock reported 2,580 detections, 51% of all "
            "traffic, and a different figure at every hour. Anchoring on log time "
            "returns 268, stable across runs and timezones.",
            1,
        ),
    ],
)

fill_section(
    16,
    "Research Paper Draft Preparation",
    [
        ("Working title", 0, True),
        ("Reproducible Rule-Based Anomaly Detection over Network Connection Logs", 1),
        ("Structure drafted", 0, True),
        (
            "Introduction; related work from the 17 surveyed papers; methodology; "
            "experimental setup; results; threats to validity; conclusion.",
            1,
        ),
        ("Status", 0, True),
        (
            "Literature survey complete and themed. Methodology and results sections "
            "drafted from the verification data. The reproducibility argument is "
            "supported by four independent published findings that detection results "
            "fail to reproduce across runs, hosts and dataset versions.",
            1,
        ),
        ("Next steps", 0, True),
        (
            "Replay the detectors against a public benchmark, CICIDS2017 or "
            "NF-UNSW-NB15, so precision and recall can be reported against published "
            "baselines, then select a target venue.",
            1,
        ),
    ],
)

# Two of the new titles wrap onto a second line, which reaches below the
# content placeholder's default top. Move the body down on those slides.
for long_title_index in (13, 14):
    placeholder = shape_by_name(slides[long_title_index], "Content Placeholder 8")
    placeholder.top = Inches(1.78)
    placeholder.height = Inches(5.06)

# --- 16: feasibility and project plan ------------------------------------
write_paragraphs(
    shape_by_name(slides[15], "TextBox 2").text_frame,
    [
        (
            "Feasibility: the system runs on a standard laptop using Python 3, SQLite, "
            "pandas, Streamlit and Plotly, all open source. Traffic is generated "
            "locally, so no data-sharing approval is required, and the full pipeline "
            "completes in 1.2 seconds over 5,000 records.",
            0,
        ),
        ("", 0),
        ("Project plan:", 0, True),
        ("Phase 1 - Literature survey and problem definition", 0),
        ("Phase 2 - Dataset design and ETL pipeline", 0),
        ("Phase 3 - Detection rules and threshold calibration", 0),
        ("Phase 4 - Dashboard and visualisation", 0),
        ("Phase 5 - Verification of determinism, idempotency and reproducibility", 0),
        ("Phase 6 - Evaluation on public benchmark traffic and final report", 0),
    ],
)

# --- 18: conclusion ------------------------------------------------------
write_paragraphs(
    shape_by_name(slides[17], "Content Placeholder 8").text_frame,
    [
        ("Summary", 0, True),
        (
            "A complete pipeline from raw connection log to explained alert, running "
            "end to end in 1.2 seconds over 5,000 records.",
            1,
        ),
        (
            "Six detectors covering port scanning, denial of service, brute force, data "
            "exfiltration, dangerous ports and hostile address ranges; 268 records "
            "flagged, a detection rate of 5.4%.",
            1,
        ),
        (
            "Detection depends on the data alone, giving identical results across runs, "
            "hosts and timezones.",
            1,
        ),
        ("Next steps for the following evaluation phase", 0, True),
        ("Replay the detectors against captured traffic and a public benchmark dataset.", 1),
        ("Baseline each host and alert on drift, replacing fixed thresholds.", 1),
        ("Add an unsupervised model as a second opinion alongside the rules.", 1),
        ("Move to streaming ingest for live alerting.", 1),
    ],
)

# --- 19: references ------------------------------------------------------
write_paragraphs(
    shape_by_name(slides[18], "Content Placeholder 8").text_frame,
    [
        ("Papers", 0, True),
        ("The seventeen papers on the Literature Survey slides, in APA format.", 1),
        ("Tools and documentation", 0, True),
        ("Python Software Foundation. Python 3 documentation. https://docs.python.org/3/", 1),
        ("SQLite Consortium. SQLite documentation. https://www.sqlite.org/docs.html", 1),
        ("The pandas development team. pandas documentation. https://pandas.pydata.org/docs/", 1),
        ("Streamlit Inc. Streamlit documentation. https://docs.streamlit.io/", 1),
        ("Plotly. Plotly Open Source Graphing Library for Python. https://plotly.com/python/", 1),
    ],
)

pres.save(DST)
print("saved", DST)
