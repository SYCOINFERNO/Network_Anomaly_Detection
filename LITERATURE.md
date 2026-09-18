# Literature Survey — Network Logs Anomaly Detection

Seventeen papers, all published 2022 or later, gathered for the PRC literature
survey and research gap tables. Each entry records the fields the review
template asks for.

**Verify every DOI before submitting.** These details were read from publisher
and arXiv pages; check each one resolves and that the venue and year match what
your department expects.

---

## Theme 1 — Datasets, reproducibility and evaluation

This theme carries the project's central claim: a detector whose result depends
on when or where it runs cannot be evaluated.

### 1. Network Intrusion Datasets: A Survey, Limitations, and Recommendations
- **Year:** 2025
- **Authors:** Patrik Goldschmidt, Daniela Chudá
- **Source:** Computers & Security, Vol. 156, Art. 104510
- **DOI:** 10.1016/j.cose.2025.104510 (arXiv:2502.06688)
- **Objective:** Systematically review public NIDS datasets and their suitability.
- **Techniques:** Systematic literature review; comparison on 13 properties.
- **Dataset used:** 89 public network intrusion datasets.
- **Parameters analysed:** Dataset properties, popularity in current research.
- **Research inference:** Data scarcity remains the field's main obstacle; many recent datasets go unused because their properties are not understood.
- **Research gap:** No agreed best practice for dataset selection, generation and reporting.

### 2. Towards Reproducible Network Traffic Analysis
- **Year:** 2022
- **Authors:** Jordan Holland, Paul Schmitt, Prateek Mittal, Nick Feamster
- **Source:** arXiv preprint
- **DOI:** 10.48550/arXiv.2203.12410
- **Objective:** Explain why traffic analysis results cannot be compared across studies.
- **Techniques:** Literature review; pcapML, which embeds metadata in raw captures.
- **Dataset used:** Public traffic analysis datasets.
- **Parameters analysed:** Dataset interpretation, metadata encoding, pipeline reproducibility.
- **Research inference:** Inconsistent dataset interpretation prevents any judgement of whether a new technique is a real advance.
- **Research gap:** No standard dataset format; bespoke pipelines block like-for-like comparison.

### 3. Confronting the Reproducibility Crisis: A Case Study of Challenges in Cybersecurity AI
- **Year:** 2024
- **Authors:** Richard H. Moulton, Gary A. McCully, John D. Hastings
- **Source:** 2024 IEEE Cyber Awareness and Research Symposium (CARS)
- **DOI:** 10.1109/CARS61786.2024.10778911
- **Objective:** Document the barriers met when reproducing published robustness results.
- **Techniques:** Case study reproduction using the VeriGauge toolkit.
- **Dataset used:** Prior published experiments.
- **Parameters analysed:** Dependencies, hardware compatibility, documentation, versioning.
- **Research inference:** Software and hardware incompatibility, version conflict and obsolescence defeat reproduction.
- **Research gap:** No infrastructure or protocol for long-term reproducibility of security AI.

### 4. SoK: Evaluations in Industrial Intrusion Detection Research
- **Year:** 2023
- **Authors:** Olav Lamberts, Konrad Wolsing, Eric Wagner, Jan Pennekamp, Jan Bauer, Klaus Wehrle, Martin Henze
- **Source:** Journal of Systems Research (JSys), Vol. 3(1)
- **DOI:** 10.5070/SR33162445
- **Objective:** Analyse how intrusion detection research evaluates its own results.
- **Techniques:** Systematic analysis of 609 publications.
- **Dataset used:** Publications' own evaluation datasets.
- **Parameters analysed:** Datasets per publication, metric choice, benchmark adoption.
- **Research inference:** Publications evaluate on 1.3 datasets on average; metrics stay ambiguous and new benchmarks go unadopted.
- **Research gap:** Fragmented evaluation hides whether the field is actually progressing.

### 5. Are We There Yet? Unraveling the State-of-the-Art Graph Network Intrusion Detection Systems
- **Year:** 2025
- **Authors:** Chenglong Wang, Pujia Zheng, Jiaping Gui, Cunqing Hua, Wajih Ul Hassan
- **Source:** arXiv preprint
- **DOI:** 10.48550/arXiv.2503.20281
- **Objective:** Reproduce and replicate published graph-based NIDS results.
- **Techniques:** Systematic re-evaluation, including under adversarial attack.
- **Dataset used:** Three public datasets and one new enterprise dataset.
- **Parameters analysed:** False positive rate, adversarial robustness.
- **Research inference:** Significant performance discrepancies appear on reproduction, traced to dataset scale, model input and implementation settings.
- **Research gap:** Reproduction and replication studies are largely absent from the field.

### 6. ConCap: Practical Network Traffic Generation for (ML- and) Flow-based Intrusion Detection Systems
- **Year:** 2025 (IEEE SaTML'26)
- **Authors:** Miel Verkerken, Laurens D'hooge, Bruno Volckaert, Filip De Turck, Giovanni Apruzzese
- **Source:** IEEE Conference on Secure and Trustworthy Machine Learning (SaTML)
- **DOI:** 10.1109/SaTML68715.2026.00051 (arXiv:2509.16038)
- **Objective:** Generate realistic, automatically labelled traffic reproducibly.
- **Techniques:** Isolated containerised scenarios driven by shareable configuration files.
- **Dataset used:** 10 network activities, 21 variants, 100 repetitions; validated against benchmarks and a real network.
- **Parameters analysed:** Flow-level equivalence to real traffic, reproducibility of scenarios.
- **Research inference:** Generated traffic is functionally equivalent to real traffic for detection purposes, and attack chains can be reproduced safely.
- **Research gap:** Thousands of prior studies rest on training data that is unobtainable or unrepresentative.

---

## Theme 2 — Explainability

This theme supports the project's choice of stated thresholds over a model.

### 7. A systematic review on the integration of explainable artificial intelligence in intrusion detection systems
- **Year:** 2025
- **Authors:** Vincent Zibi Mohale, Ibidun Christiana Obagbuwa
- **Source:** Frontiers in Artificial Intelligence
- **DOI:** 10.3389/frai.2025.1526221
- **Objective:** Review how XAI addresses the black-box problem in IDS.
- **Techniques:** SHAP, LIME, decision trees, rule-based and hybrid models.
- **Dataset used:** CICIDS-2017, KDD Cup 99 (as reported across reviewed studies).
- **Parameters analysed:** Accuracy, false positive rate, interpretability, computational cost, time to response.
- **Research inference:** Model-agnostic XAI helps, but overhead and the interpretability-accuracy trade-off block real-time deployment.
- **Research gap:** No standard interpretability metric; no lightweight real-time explanation method.

### 8. Evaluating the Explainability of State-of-the-Art Deep Learning-based Network Intrusion Detection Systems
- **Year:** 2024
- **Authors:** Ayush Kumar, Vrizlynn L. L. Thing
- **Source:** arXiv preprint
- **DOI:** 10.48550/arXiv.2408.14040
- **Objective:** Assess whether DL-based NIDS decisions can be explained.
- **Techniques:** Conventional and recent XAI tools; new criteria for global/local agreement.
- **Dataset used:** Several attack datasets.
- **Parameters analysed:** Explainability per model, agreement between XAI tools, security-focused metrics.
- **Research inference:** XAI tools disagree with each other on most models; explainability must be traded against detection performance.
- **Research gap:** Prior XAI evaluation ignored state-of-the-art DL NIDS.

### 9. Classification and Explanation of Distributed Denial-of-Service (DDoS) Attack Detection using Machine Learning and Shapley Additive Explanation (SHAP) Methods
- **Year:** 2023
- **Authors:** Yuanyuan Wei, Julian Jang-Jaccard, Amardeep Singh, Fariza Sabrina, Seyit Camtepe
- **Source:** arXiv preprint
- **DOI:** 10.48550/arXiv.2306.17190
- **Objective:** Classify DDoS traffic and explain the classification.
- **Techniques:** XGBoost SHAP feature selection (top 20 features); MLP classifier.
- **Dataset used:** A DDoS attack dataset.
- **Parameters analysed:** Feature importance, accuracy.
- **Research inference:** Selected features reach above 99% accuracy while keeping explanations available.
- **Research gap:** Interpretability of security models is asserted as necessary but not yet standardised.

---

## Theme 3 — Detection methods and rule design

### 10. Ruling the Unruly: Designing Effective, Low-Noise Network Intrusion Detection Rules for Security Operations Centers
- **Year:** 2025
- **Authors:** Koen T. W. Teuwen, Tom Mulders, Emmanuele Zambon, Luca Allodi
- **Source:** ACM (ASIA CCS proceedings)
- **DOI:** 10.1145/3708821.3710823
- **Objective:** Identify what makes a signature-based detection rule good.
- **Techniques:** Empirical characterisation of deployed rules; interviews with rule designers; quantitative validation.
- **Dataset used:** Rules and alerts from a commercial managed SOC.
- **Parameters analysed:** Rule specificity, analyst workload, alert throttling, coverage.
- **Research inference:** Six design principles affect rule quality; rules matching generalised characteristics raise both coverage and workload.
- **Research gap:** How to keep coverage while cutting analyst workload is unresolved.

### 11. Ensemble Defense System: A Hybrid IDS Approach for Effective Cyber Threat Detection
- **Year:** 2023
- **Authors:** Sarah Alharbi, Arshiya Khan
- **Source:** 33rd International Telecommunication Networks and Applications Conference (ITNAC), pp. 267-270
- **DOI:** 10.1109/ITNAC59571.2023.10368510
- **Objective:** Combine signature-based and anomaly-based detection in one framework.
- **Techniques:** Suricata and Zeek (signature), Slips (anomaly), Elasticsearch (SIEM).
- **Dataset used:** Scripted attacks: port scanning, privilege escalation, denial of service.
- **Parameters analysed:** Detection across attack categories.
- **Research inference:** The hybrid framework detected every tested attack category.
- **Research gap:** No evaluation of alert volume or false positives at scale.

### 12. Anomaly detection in network flows using unsupervised online machine learning
- **Year:** 2025
- **Authors:** Alberto Miguel-Diez, Adrián Campazas-Vega, Ángel Manuel Guerrero-Higueras, Claudia Álvarez-Aparicio, Vicente Matellán-Olivera
- **Source:** arXiv preprint
- **DOI:** 10.48550/arXiv.2509.01375
- **Objective:** Detect anomalies in flows without labelled training data.
- **Techniques:** Online One-Class SVM using the River library.
- **Dataset used:** NF-UNSW-NB15 and NF-UNSW-NB15-v2.
- **Parameters analysed:** Accuracy (>98%), false positive rate (<3.1%), recall, latency (<0.033 ms per flow).
- **Research inference:** Online unsupervised detection is fast enough for real-time monitoring.
- **Research gap:** Generalisation across network environments not established.

### 13. Machine learning-based network intrusion detection for big and imbalanced data using oversampling, stacking feature embedding and feature extraction
- **Year:** 2024
- **Authors:** Md. Alamin Talukder, Md. Manowarul Islam, Md Ashraf Uddin, Khondokar Fida Hasan, Selina Sharmin, Salem A. Alyami, Mohammad Ali Moni
- **Source:** Journal of Big Data (arXiv:2401.12262)
- **DOI:** 10.48550/arXiv.2401.12262
- **Objective:** Handle class imbalance in large intrusion detection datasets.
- **Techniques:** Random oversampling, stacking feature embedding, PCA, Decision Tree / Random Forest / Extra Trees.
- **Dataset used:** UNSW-NB15, CIC-IDS2017, CIC-IDS2018.
- **Parameters analysed:** Accuracy per dataset and classifier.
- **Research inference:** Reported accuracy 99.59-99.99% across the three datasets.
- **Research gap:** Accuracy this high on benchmark data invites questions about leakage and dataset artefacts.

### 14. An Adversarial Robustness Benchmark for Enterprise Network Intrusion Detection
- **Year:** 2024
- **Authors:** João Vitorino, Miguel Silva, Eva Maia, Isabel Praça
- **Source:** Foundations and Practice of Security (FPS 2023)
- **DOI:** 10.1007/978-3-031-57537-2_1
- **Objective:** Compare model robustness under standardised adversarial conditions.
- **Techniques:** Random Forest, XGBoost, LightGBM, Explainable Boosting Machine; regular and adversarial training.
- **Dataset used:** CICIDS2017, NewCICIDS, HIKARI.
- **Parameters analysed:** Robustness to constrained adversarial examples, false alarm rate, generalisation.
- **Research inference:** The corrected NewCICIDS improved results; adversarial training raised robustness without harming normal detection.
- **Research gap:** Transferability across different enterprise environments untested.

---

## Theme 4 — Surveys of the field

### 15. Deep Learning-based Intrusion Detection Systems: A Survey
- **Year:** 2025
- **Authors:** Zhiwei Xu, Yujuan Wu, Shiheng Wang, Jiabao Gao, Tian Qiu, Ziqi Wang, Hai Wan, Xibin Zhao
- **Source:** arXiv preprint
- **DOI:** 10.48550/arXiv.2504.07839
- **Objective:** Survey the full deep-learning IDS pipeline.
- **Techniques:** Review across collection, log storage, parsing, graph summarisation, detection, investigation.
- **Dataset used:** Public benchmark datasets for DL-IDS.
- **Parameters analysed:** Generalisation, zero-day detection.
- **Research inference:** Deep learning generalises beyond signature matching but the pipeline stages are studied in isolation.
- **Research gap:** Open challenges across every pipeline stage remain unaddressed.

### 16. Network Intrusion Detection: Evolution from Conventional Approaches to LLM Collaboration and Emerging Risks
- **Year:** 2025
- **Authors:** Yaokai Feng, Kouichi Sakurai
- **Source:** arXiv preprint
- **DOI:** 10.48550/arXiv.2510.23313
- **Objective:** Trace NIDS development from signatures through neural networks to LLMs.
- **Techniques:** Literature review across conventional, vehicular and IoT settings.
- **Dataset used:** Reviewed studies' own datasets.
- **Parameters analysed:** Signature effectiveness, NN deployment difficulty, LLM benefit and dual-use risk.
- **Research inference:** Signature-based methods retain value; neural detection still meets deployment obstacles.
- **Research gap:** Practical LLM deployment and LLM-enabled attack vectors are open problems.

### 17. Evaluating Machine Learning-Driven Intrusion Detection Systems in IoT: Performance and Energy Consumption
- **Year:** 2025
- **Authors:** Saeid Jamshidi, Kawser Wazed Nafi, Amin Nikanjam, Foutse Khomh
- **Source:** Computers & Industrial Engineering
- **DOI:** 10.1016/j.cie.2025.111103 (arXiv:2504.09634)
- **Objective:** Measure the cost of running ML-based IDS at the network edge.
- **Techniques:** Empirical comparison of classical ML and deep learning IDS, with and without SDN; ANOVA.
- **Dataset used:** Edge deployment under benign and attack conditions.
- **Parameters analysed:** CPU load, CPU usage, energy consumption.
- **Research inference:** Edge-deployed ML IDS raise resource consumption sharply during attacks.
- **Research gap:** Little prior work measures IDS cost under real-time threat in constrained environments.

---

## How these support the project

| Claim in the project | Supported by |
|---|---|
| Detection must not depend on run time or host | 2, 3, 5 |
| Datasets and their construction must be stated and reproducible | 1, 2, 6 |
| Synthesised attack traffic must preserve temporal structure | 6, 12 |
| Rule-based detection remains defensible against ML | 10, 11, 16 |
| Alerts must be explainable to be actionable | 7, 8, 9 |
| Benchmark accuracy near 100% deserves suspicion | 4, 13, 14 |
| Detector cost matters on modest hardware | 17, 12 |
