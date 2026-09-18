const pptxgen = require("pptxgenjs");

// ---------------------------------------------------------------- palette
const NAVY_DEEP = "0F1B33"; // dark slide background
const NAVY = "1E2761"; // dominant brand tone
const NAVY_SOFT = "2E3F7F"; // lighter navy for secondary fills
const ICE = "CADCFC"; // secondary, light accents on dark
const ICE_TINT = "EEF3FC"; // card tint on light slides
const WHITE = "FFFFFF";
const ALERT = "E0443E"; // sharp accent: anomalies
const ALERT_SOFT = "FBE9E8"; // alert card tint
const INK = "17203A"; // body text on light
const MUTED = "5B6788"; // captions

const HEAD = "Cambria";
const BODY = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" x 5.625"
pres.author = "Final Year Project";
pres.title = "Network Logs Anomaly Detection";

const W = 10,
  M = 0.5,
  CW = 9.0; // slide width, margin, content width

// fresh options object every call — pptxgenjs mutates these in place
const softShadow = () => ({
  type: "outer",
  color: "1E2761",
  opacity: 0.14,
  blur: 8,
  offset: 2,
  angle: 90,
});

function card(slide, x, y, w, h, fill) {
  slide.addShape(pres.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.08,
    fill: { color: fill || ICE_TINT },
    line: { color: fill || ICE_TINT },
    shadow: softShadow(),
  });
}

function dot(slide, x, y, d, fill, label, labelColor, labelSize) {
  slide.addShape(pres.ShapeType.ellipse, {
    x,
    y,
    w: d,
    h: d,
    fill: { color: fill },
    line: { color: fill },
  });
  if (label) {
    slide.addText(label, {
      x,
      y,
      w: d,
      h: d,
      isTextBox: true,
      margin: 0,
      align: "center",
      valign: "middle",
      fontFace: BODY,
      fontSize: labelSize || 13,
      bold: true,
      color: labelColor || WHITE,
    });
  }
}

function title(slide, text, color) {
  slide.addText(text, {
    x: M,
    y: 0.42,
    w: CW,
    h: 0.75,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 36,
    bold: true,
    color: color || NAVY,
  });
}

function kicker(slide, text, color) {
  slide.addText(text.toUpperCase(), {
    x: M,
    y: 1.15,
    w: CW,
    h: 0.28,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 11,
    bold: true,
    charSpacing: 2,
    color: color || MUTED,
  });
}

// ============================================================ 1 — title
{
  const s = pres.addSlide();
  s.background = { color: NAVY_DEEP };

  s.addText("Network Logs", {
    x: 0.7,
    y: 1.42,
    w: 5.9,
    h: 0.72,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 40,
    bold: true,
    color: WHITE,
  });
  s.addText("Anomaly Detection", {
    x: 0.7,
    y: 2.12,
    w: 5.9,
    h: 0.72,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 40,
    bold: true,
    color: ICE,
  });
  s.addText(
    "An ETL and rule-based detection pipeline over a week of network traffic",
    {
      x: 0.7,
      y: 2.98,
      w: 5.6,
      h: 0.6,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 15,
      color: ICE,
    }
  );
  s.addText("Final Year Project  ·  Computer Science", {
    x: 0.7,
    y: 4.32,
    w: 5.6,
    h: 0.3,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 11,
    bold: true,
    charSpacing: 2,
    color: MUTED,
  });

  // motif: a field of connections, a handful of them hostile
  const alertCells = [3, 9, 14, 22, 27, 31];
  let i = 0;
  for (let r = 0; r < 6; r++) {
    for (let c = 0; c < 6; c++) {
      const hostile = alertCells.indexOf(i) !== -1;
      dot(
        s,
        6.95 + c * 0.42,
        1.5 + r * 0.42,
        0.24,
        hostile ? ALERT : "26355E"
      );
      i++;
    }
  }
  s.addText("6 of 36 connections hostile", {
    x: 6.95,
    y: 4.18,
    w: 2.6,
    h: 0.3,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 11,
    italic: true,
    color: MUTED,
  });

  s.addNotes(
    "Introduce the project: network connection logs are generated faster than anyone can read them. This system ingests a week of traffic and flags the connections worth investigating."
  );
}

// ========================================================== 2 — problem
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "The Problem");
  kicker(s, "Why detection has to be automated");

  s.addText(
    [
      {
        text: "Every connection a network makes leaves a log line: who talked to whom, on which port, for how long, and how many bytes moved.",
        options: { breakLine: true, paraSpaceAfter: 10 },
      },
      {
        text: "An intrusion is visible in those lines — but only as a pattern across many of them. A single connection to port 22 is routine. Forty of them in four minutes is an attack.",
        options: { breakLine: true, paraSpaceAfter: 10 },
      },
      {
        text: "Reading a week of logs by hand is not feasible, and the pattern is invisible line by line in any case.",
        options: {},
      },
    ],
    {
      x: M,
      y: 1.72,
      w: 5.1,
      h: 3.1,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 14.5,
      color: INK,
      lineSpacingMultiple: 1.15,
      valign: "top",
    }
  );

  const stats = [
    ["5,000", "connection records across seven days", ICE_TINT, NAVY, INK],
    ["268", "flagged for investigation, 5.4%", ALERT_SOFT, ALERT, INK],
  ];
  stats.forEach((st, idx) => {
    const y = 1.72 + idx * 1.62;
    card(s, 5.95, y, 3.55, 1.38, st[2]);
    s.addText(st[0], {
      x: 6.2,
      y: y + 0.13,
      w: 3.05,
      h: 0.7,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 44,
      bold: true,
      color: st[3],
    });
    s.addText(st[1], {
      x: 6.2,
      y: y + 0.86,
      w: 3.05,
      h: 0.4,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      color: st[4],
    });
  });

  s.addNotes(
    "The key point for the examiner: an attack is a property of a group of connections in a time window, not of any single record. That is what makes rule-based detection over windows the right tool."
  );
}

// ========================================================= 3 — pipeline
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "System Architecture");
  kicker(s, "Four stages, one direction of flow");

  const stages = [
    [
      "Generate",
      "5,000 synthetic records over seven days, mixing normal traffic with simulated attacks",
    ],
    [
      "Load",
      "Timestamps normalised, records inserted into SQLite, indexes built on time, source and destination",
    ],
    [
      "Detect",
      "Six rules evaluate each record against the traffic preceding it; matches are written with type and severity",
    ],
    [
      "Display",
      "Streamlit dashboard with metrics, filters, traffic analysis and a threat heatmap",
    ],
  ];

  stages.forEach((st, idx) => {
    const x = 0.5 + idx * 2.3;
    card(s, x, 1.85, 2.0, 2.75, idx === 2 ? ALERT_SOFT : ICE_TINT);
    dot(
      s,
      x + 0.22,
      2.07,
      0.46,
      idx === 2 ? ALERT : NAVY,
      String(idx + 1),
      WHITE,
      14
    );
    s.addText(st[0], {
      x: x + 0.22,
      y: 2.66,
      w: 1.56,
      h: 0.32,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 18,
      bold: true,
      color: idx === 2 ? ALERT : NAVY,
    });
    s.addText(st[1], {
      x: x + 0.22,
      y: 3.04,
      w: 1.56,
      h: 1.4,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 10.5,
      color: INK,
      lineSpacingMultiple: 1.1,
      valign: "top",
    });
  });

  s.addNotes(
    "Walk left to right. Each stage is a separate module in src/: log_generator.py, database.py, anomaly_detector.py, dashboard.py. Stage three is where the contribution sits."
  );
}

// ========================================================== 4 — dataset
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Dataset Design");
  kicker(s, "Attacks are emitted as bursts, not scattered singles");

  const items = [
    ["DDoS flood", "160 connections to one host inside 40 seconds", ALERT],
    ["Port scan", "Two campaigns, 25 distinct ports each over 150 seconds", ALERT],
    ["Brute force", "35 attempts on port 22 against one host over 4 minutes", ALERT],
    ["Data exfiltration", "Three campaigns moving 15-24 MB outbound each", ALERT],
    ["Legacy services", "12 isolated connections to Telnet, SMB and RDP", NAVY_SOFT],
    ["Normal traffic", "4,725 ordinary outbound connections filling the week", NAVY],
  ];

  items.forEach((it, idx) => {
    const col = idx % 3,
      row = Math.floor(idx / 3);
    const x = 0.5 + col * 3.1,
      y = 1.76 + row * 1.62;
    card(s, x, y, 2.8, 1.32, it[2] === ALERT ? ALERT_SOFT : ICE_TINT);
    dot(s, x + 0.22, y + 0.2, 0.3, it[2]);
    s.addText(it[0], {
      x: x + 0.6,
      y: y + 0.19,
      w: 2.0,
      h: 0.32,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 15,
      bold: true,
      color: NAVY,
    });
    s.addText(it[1], {
      x: x + 0.22,
      y: y + 0.6,
      w: 2.36,
      h: 0.64,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11,
      color: INK,
      lineSpacingMultiple: 1.1,
      valign: "top",
    });
  });

  s.addText(
    "Temporal density is the signal. Scattered attack records form no pattern and no rule can recover one.",
    {
      x: M,
      y: 5.0,
      w: CW,
      h: 0.3,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11,
      italic: true,
      color: MUTED,
    }
  );

  s.addNotes(
    "This was a real defect found during testing. The first generator scattered attack records uniformly across seven days, so four of the six rules never fired. Clustering them into campaigns fixed it."
  );
}

// ============================================================ 5 — rules
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Six Detection Rules");
  kicker(s, "Each match carries a type, a severity and a description");

  const rules = [
    ["Port scanning", "More than 10 distinct ports from one source in 5 min", "MED"],
    ["DDoS", "More than 100 connections to one host in 60 sec", "HIGH"],
    ["Brute force", "More than 20 attempts on port 22 in 5 min", "HIGH"],
    ["Data exfiltration", "More than 10 MB sent by one host in 10 min", "CRIT"],
    ["Uncommon port", "Traffic to Telnet, SMB, RDP, SQL Server, MongoDB", "LOW"],
    ["Suspicious IP", "Source address inside a known-hostile range", "MED"],
  ];
  const sevColor = { CRIT: ALERT, HIGH: "C2562F", MED: NAVY_SOFT, LOW: MUTED };

  rules.forEach((r, idx) => {
    const col = idx % 2,
      row = Math.floor(idx / 2);
    const x = 0.5 + col * 4.65,
      y = 1.8 + row * 1.25;
    dot(s, x, y + 0.06, 0.44, sevColor[r[2]], String(idx + 1), WHITE, 13);
    s.addText(r[0], {
      x: x + 0.58,
      y: y,
      w: 2.4,
      h: 0.3,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 16,
      bold: true,
      color: NAVY,
    });
    s.addText(r[2], {
      x: x + 3.0,
      y: y + 0.03,
      w: 0.85,
      h: 0.26,
      isTextBox: true,
      margin: 0,
      align: "right",
      fontFace: BODY,
      fontSize: 10,
      bold: true,
      charSpacing: 1,
      color: sevColor[r[2]],
    });
    s.addText(r[1], {
      x: x + 0.58,
      y: y + 0.34,
      w: 3.27,
      h: 0.55,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11.5,
      color: INK,
      lineSpacingMultiple: 1.1,
      valign: "top",
    });
  });

  s.addNotes(
    "Rules are evaluated in order and the first match wins, so every flagged record has exactly one classification. Thresholds are parameters on each method, not constants buried in SQL."
  );
}

// ====================================================== 6 — correctness
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Getting the Window Right");
  kicker(s, "The correctness problem at the centre of the project");

  card(s, 0.5, 1.78, 4.35, 2.72, ALERT_SOFT);
  dot(s, 0.78, 2.02, 0.34, ALERT);
  s.addText("Anchored on wall-clock time", {
    x: 1.24,
    y: 2.0,
    w: 3.4,
    h: 0.32,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 16,
    bold: true,
    color: ALERT,
  });
  s.addText(
    [
      { text: "timestamp > datetime('now', '-60 seconds')", options: { breakLine: true, fontFace: "Courier New", fontSize: 11, paraSpaceAfter: 8 } },
      { text: "Log times were local, datetime('now') is UTC. The 5.5 hour gap let almost every record satisfy the window.", options: { breakLine: true, paraSpaceAfter: 8 } },
      { text: "Result: 2,580 anomalies — 51% of all traffic — and a different answer at every hour of the day.", options: {} },
    ],
    {
      x: 0.78,
      y: 2.46,
      w: 3.8,
      h: 1.85,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      color: INK,
      lineSpacingMultiple: 1.12,
      valign: "top",
    }
  );

  card(s, 5.15, 1.78, 4.35, 2.72, ICE_TINT);
  dot(s, 5.43, 2.02, 0.34, NAVY);
  s.addText("Anchored on log time", {
    x: 5.89,
    y: 2.0,
    w: 3.4,
    h: 0.32,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 16,
    bold: true,
    color: NAVY,
  });
  s.addText(
    [
      { text: "timestamp > datetime(?, ?) AND timestamp <= ?", options: { breakLine: true, fontFace: "Courier New", fontSize: 11, paraSpaceAfter: 8 } },
      { text: "The window ends at the timestamp of the record being examined, so the query reads only what preceded it.", options: { breakLine: true, paraSpaceAfter: 8 } },
      { text: "Result: 268 anomalies — 5.4% — identical on every run, in any timezone.", options: {} },
    ],
    {
      x: 5.43,
      y: 2.46,
      w: 3.8,
      h: 1.85,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      color: INK,
      lineSpacingMultiple: 1.12,
      valign: "top",
    }
  );

  s.addText(
    "A detector whose output depends on when it runs cannot be evaluated, tuned or trusted.",
    {
      x: M,
      y: 4.68,
      w: CW,
      h: 0.32,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      italic: true,
      color: MUTED,
    }
  );

  s.addNotes(
    "Expect a question here. The fix has two halves: store timestamps in SQLite's own format so string comparison is valid, and pass the record's own timestamp as the window anchor instead of calling datetime('now')."
  );
}

// ========================================================== 7 — results
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Results");
  kicker(s, "A representative run over 5,000 records");

  s.addChart(
    pres.ChartType.bar,
    [
      {
        name: "Detections",
        labels: [
          "Brute force",
          "Suspicious IP",
          "DDoS",
          "Port scan",
          "Uncommon port",
          "Exfiltration",
        ],
        values: [79, 74, 61, 30, 13, 11],
      },
    ],
    {
      x: 0.4,
      y: 1.66,
      w: 5.85,
      h: 3.4,
      barDir: "bar",
      showTitle: true,
      title: "Detections by rule",
      titleFontFace: HEAD,
      titleFontSize: 13,
      titleColor: NAVY,
      chartColors: [NAVY],
      showValue: true,
      dataLabelPosition: "outEnd",
      dataLabelFontFace: BODY,
      dataLabelFontSize: 10,
      dataLabelColor: INK,
      showLegend: false,
      catAxisLabelFontFace: BODY,
      catAxisLabelFontSize: 10,
      catAxisLabelColor: INK,
      valAxisLabelFontFace: BODY,
      valAxisLabelFontSize: 9,
      valAxisLabelColor: MUTED,
      valGridLine: { color: "E4E9F2", size: 1 },
      catGridLine: { style: "none" },
      barGapWidthPct: 45,
    }
  );

  const stats = [
    ["268", "anomalies flagged", NAVY],
    ["5.4%", "of all traffic", NAVY],
    ["1.2 s", "full pipeline runtime", ALERT],
  ];
  stats.forEach((st, idx) => {
    const y = 1.72 + idx * 1.16;
    card(s, 6.45, y, 3.05, 0.98, idx === 2 ? ALERT_SOFT : ICE_TINT);
    s.addText(st[0], {
      x: 6.68,
      y: y + 0.08,
      w: 2.6,
      h: 0.5,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 30,
      bold: true,
      color: st[2],
    });
    s.addText(st[1], {
      x: 6.68,
      y: y + 0.6,
      w: 2.6,
      h: 0.28,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11,
      color: INK,
    });
  });

  s.addNotes(
    "All six rules fire. Severity splits 140 high, 104 medium, 13 low, 11 critical. Across three independent generate-and-detect runs the total was 267, 267 and 268."
  );
}

// ======================================================== 8 — dashboard
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "The Dashboard");
  kicker(s, "Five views over the same detection output");

  const tabs = [
    ["Overview", "Headline metrics: connections, anomalies, unique sources, volume"],
    ["Anomalies", "Filter and search detections by type, severity and address"],
    ["Traffic analysis", "Volume and protocol breakdowns over the week"],
    ["Threat heatmap", "Where and when hostile activity concentrates"],
    ["Log viewer", "The underlying records behind any figure on screen"],
  ];

  tabs.forEach((t, idx) => {
    const y = 1.76 + idx * 0.68;
    dot(s, 0.5, y, 0.42, NAVY, String(idx + 1), WHITE, 12);
    s.addText(t[0], {
      x: 1.06,
      y: y + 0.01,
      w: 1.95,
      h: 0.3,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 15,
      bold: true,
      color: NAVY,
    });
    s.addText(t[1], {
      x: 3.05,
      y: y + 0.03,
      w: 3.55,
      h: 0.42,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11.5,
      color: INK,
      lineSpacingMultiple: 1.05,
      valign: "top",
    });
  });

  card(s, 7.0, 1.76, 2.5, 3.24, ICE_TINT);
  s.addText("Live", {
    x: 7.25,
    y: 2.0,
    w: 2.0,
    h: 0.55,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 34,
    bold: true,
    color: NAVY,
  });
  s.addText(
    "Every view reads the same database the detector writes. Nothing is recomputed for display, so the dashboard cannot disagree with the pipeline.",
    {
      x: 7.25,
      y: 2.62,
      w: 2.0,
      h: 1.6,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11,
      color: INK,
      lineSpacingMultiple: 1.12,
      valign: "top",
    }
  );
  s.addText("localhost:8501", {
    x: 7.25,
    y: 4.5,
    w: 2.0,
    h: 0.3,
    isTextBox: true,
    margin: 0,
    fontFace: "Courier New",
    fontSize: 11,
    color: MUTED,
  });

  s.addNotes(
    "Demonstrate live if possible: streamlit run src/dashboard.py. The dashboard reads the same SQLite database the detector writes, so nothing is recomputed for display."
  );
}

// ======================================================= 9 — guarantees
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Engineering Guarantees");
  kicker(s, "Properties the system holds, and how they were verified");

  const items = [
    [
      "Deterministic",
      "Detection windows measure log time, never wall-clock time. Three independent runs returned 267, 267 and 268.",
    ],
    [
      "Idempotent",
      "Processed record identifiers are tracked, so re-running the detector over a scanned database adds nothing.",
    ],
    [
      "Reproducible",
      "Seeding the generator produces a byte-identical dataset, verified by matching MD5 digests.",
    ],
    [
      "Injection-safe",
      "Every query is parameterised. No address, port or threshold is interpolated into SQL as a string.",
    ],
  ];

  items.forEach((it, idx) => {
    const col = idx % 2,
      row = Math.floor(idx / 2);
    const x = 0.5 + col * 4.65,
      y = 1.85 + row * 1.66;
    card(s, x, y, 4.35, 1.45, ICE_TINT);
    dot(s, x + 0.26, y + 0.22, 0.32, NAVY);
    s.addText(it[0], {
      x: x + 0.7,
      y: y + 0.2,
      w: 3.4,
      h: 0.32,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 16,
      bold: true,
      color: NAVY,
    });
    s.addText(it[1], {
      x: x + 0.26,
      y: y + 0.64,
      w: 3.84,
      h: 0.64,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11.5,
      color: INK,
      lineSpacingMultiple: 1.1,
      valign: "top",
    });
  });

  s.addNotes(
    "These four are the difference between a script that produces a number and a detector whose number means something. Each was checked, not assumed."
  );
}

// ============================================================ 10 — stack
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Technology");
  kicker(s, "Chosen for transparency over convenience");

  const stack = [
    ["Python 3", "Pipeline and rules"],
    ["SQLite", "Storage and indexes"],
    ["pandas", "Record handling"],
    ["Streamlit", "Dashboard"],
    ["Plotly", "Charts"],
  ];

  stack.forEach((t, idx) => {
    const x = 0.5 + idx * 1.85;
    dot(s, x + 0.32, 1.9, 0.86, idx < 3 ? NAVY : NAVY_SOFT);
    s.addText(t[0], {
      x: x,
      y: 2.94,
      w: 1.5,
      h: 0.3,
      isTextBox: true,
      margin: 0,
      align: "center",
      fontFace: HEAD,
      fontSize: 15,
      bold: true,
      color: NAVY,
    });
    s.addText(t[1], {
      x: x,
      y: 3.26,
      w: 1.5,
      h: 0.3,
      isTextBox: true,
      margin: 0,
      align: "center",
      fontFace: BODY,
      fontSize: 10.5,
      color: MUTED,
    });
  });

  card(s, 0.5, 3.92, 9.0, 1.08, ICE_TINT);
  s.addText(
    [
      { text: "Rules over machine learning.  ", options: { bold: true } },
      {
        text: "Every detection can be traced to a threshold and explained to the person acting on it. A model that flags a connection without a reason is of little use to an analyst who must decide whether to block it.",
        options: {},
      },
    ],
    {
      x: 0.78,
      y: 4.08,
      w: 8.44,
      h: 0.76,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      color: INK,
      lineSpacingMultiple: 1.1,
      valign: "top",
    }
  );

  s.addNotes(
    "If asked why not machine learning: the dataset has labels, so supervised learning is possible, but an unexplainable flag is operationally weak. Rules also give a baseline any model would have to beat."
  );
}

// ======================================================= 11 — conclusion
{
  const s = pres.addSlide();
  s.background = { color: NAVY_DEEP };

  s.addText("What the Project Shows", {
    x: M,
    y: 0.52,
    w: CW,
    h: 0.7,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 34,
    bold: true,
    color: WHITE,
  });

  const outcomes = [
    "A complete pipeline from raw log to explained alert, running end to end in 1.2 seconds",
    "Detection that depends on the data alone — same input, same output, any machine, any hour",
    "Six attack classes recognised by their shape in time, each traceable to a stated threshold",
  ];
  outcomes.forEach((o, idx) => {
    const y = 1.6 + idx * 0.82;
    dot(s, M, y + 0.03, 0.3, ICE);
    s.addText(o, {
      x: 1.0,
      y: y,
      w: 4.55,
      h: 0.7,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13,
      color: WHITE,
      lineSpacingMultiple: 1.12,
      valign: "top",
    });
  });

  card(s, 6.0, 1.52, 3.5, 2.6, "1A2747");
  s.addText("Where it goes next", {
    x: 6.3,
    y: 1.74,
    w: 2.9,
    h: 0.32,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 16,
    bold: true,
    color: ICE,
  });
  s.addText(
    [
      { text: "Replay against captured traffic", options: { bullet: true, breakLine: true, paraSpaceAfter: 7 } },
      { text: "Baseline each host, alert on drift", options: { bullet: true, breakLine: true, paraSpaceAfter: 7 } },
      { text: "Unsupervised model as a second opinion", options: { bullet: true, breakLine: true, paraSpaceAfter: 7 } },
      { text: "Streaming ingest for live alerting", options: { bullet: true } },
    ],
    {
      x: 6.3,
      y: 2.2,
      w: 2.9,
      h: 1.75,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11.5,
      color: WHITE,
      lineSpacingMultiple: 1.08,
      valign: "top",
    }
  );

  s.addText("Thank you  ·  Questions welcome", {
    x: M,
    y: 4.62,
    w: CW,
    h: 0.32,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 12,
    bold: true,
    charSpacing: 1,
    color: MUTED,
  });

  s.addNotes(
    "Close on the guarantee, not the feature list: the number this system reports means the same thing tomorrow as it does today. Then invite questions."
  );
}

pres
  .writeFile({
    fileName: "D:/Final_project/network_anomaly_detection/Network_Anomaly_Detection.pptx",
  })
  .then((f) => console.log("written:", f));
