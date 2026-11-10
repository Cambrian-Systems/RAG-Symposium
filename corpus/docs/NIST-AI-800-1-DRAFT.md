---
id: "NIST-AI-800-1-DRAFT"
aliases: ["NIST AI 800-1", "AI 800-1 second public draft", "Managing Misuse Risk for Dual-Use Foundation Models"]
title: "Managing Misuse Risk for Dual-Use Foundation Models (Second Public Draft)"
issuer: "National Institute of Standards and Technology (U.S. AI Safety Institute)"
published: "2025-01"
revised: ""
status: "draft"
status_note: "Second public draft. We found no final version."
status_evidence: "PDF cover: \"NIST AI 800-1 2pd ... Second Public Draft ... Managing Misuse Risk for Dual-Use Foundation Models ... U.S. AI Safety Institute\" — https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-1.ipd2.pdf"
replaces: []
replaced_by: []
topics: ["security", "standards"]
source_url: "https://www.nist.gov/publications/managing-misuse-risk-dual-use-foundation-models"
credit: "National Institute of Standards and Technology (U.S. AI Safety Institute), Managing Misuse Risk for Dual-Use Foundation Models (Second Public Draft), 2025-01."
license_note: "U.S. government work; not subject to copyright in the United States (17 U.S.C. 105)."
---

<!-- page 1 -->
NIST AI 800-1 2pd 1
Second Public Draft 2
Managing Misuse Risk for Dual-Use 3
Foundation Models 4
5
U.S. AI Safety Institute 6
This publication is available free of charge from: 7
https://doi.org/10.6028/NIST.AI.800-1.2pd 8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24

<!-- page 2 -->
NIST AI 800-1 2pd 1
Second Public Draft 2
Managing Misuse Risk for Dual-Use 3
Foundation Models4
5
U.S. AI Safety Institute 6
7
This publication is available free of charge from: 8
https://doi.org/10.6028/NIST.AI.800-1.2pd 9
January 2025 10
11
12
13
14
15
16
17
18
19
20 21
U.S. Department of Commerce  22
Gina M. Raimondo, Secretary 23
24 National Institute of Standards and Technology
 Charles H. Romine, Acting Under Secretary of Commerce for Standards and Technology and Acting NIST Director  25
26
27
28
29

<!-- page 3 -->
NIST AI 800-1 2pd (Second Public Draft) Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute
The U.S. AI Safety Institute (AISI) at NIST is releasing this document as an updated draft 1
for the second round of public comment.  2
3
Comments on NIST AI 800-1 2pd may be sent electronically to NISTAI800-1@nist.gov with 4
“NIST AI 800-1 2pd, Managing Misuse Risk for Dual-Use Foundation Models” in the subject 5
line. Electronic submissions may be sent as an attachment in any of the following unlocked 6
formats: HTML; ASCII; Word; RTF; or PDF. 7
8
All comments are subject to release under the Freedom of Information Act (FOIA)9

<!-- page 4 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

Contents 1
1. INTRODUCTION ................................ ................................ ................................ .............................. 1 2
2. SCOPE ................................ ................................ ................................ ................................ ............1 3
3. MISUSE RISK MANAGEMENT THROUGHOUT THE AI SUPPLY CHAIN ................................ .................2 4
4. KEY CHALLENGES IN MANAGING MISUSE RISKS................................ ................................ ...............4 5
5. OBJECTIVES AND PRACTICES TO MANAGE MISUSE RISKS ................................ ................................ .6 6
7
8
9
10
11
12
13
Appendix A. Glossary ................................ ................................ ................................ .......................  22 14
Appendix B. Example Methods to Mitigate Misuse Risk ................................ ................................ .... 24 15
Appendix C. Key Characteristics of Measurement Tasks ................................ ................................ .... 26 16
Appendix D. Application of NIST AI 800-1 to Chemical and Biological Misuse Risk ..............................  31 17
Appendix E: Application of NIST AI 800-1 to Cyber Misuse Risk ................................ ..........................  47 18
 19
Disclaimer: Certain equipment, instruments, software, or materials, commercial or non-commercial, are 20
identified in this paper in order to specify the experimental procedure adequately. Such identification 21
does not imply recommendation or endorsement of any product or service by NIST, nor does it imply that 22
the materials or equipment identified are necessarily the best available for the purpose.23

<!-- page 5 -->
1. INTRODUCTION 1
This document provides voluntary guidelines for improving the safety, security, and 2
trustworthiness of dual-use foundation modelsi (hereafter referred to as “foundation models”)ii 3
consistent with the National AI Initiative Act,iii Executive Order 14110,iv and the October 24, 4
2024, Presidential National Security Memorandum on AI.v,1 Specifically, it focuses on managing 5
the risk that such models will be deliberately misused to cause harm to public safety or national 6
security. The ways that foundation models can be misused continue to evolve, but scenarios 7
include using a model to facilitate the development of chemical, biological, radiological, or 8
nuclear weapons; enable offensive cyber-attacks; and generate harmful or dangerous content, 9
such as child sexual abuse material (CSAM) and non-consensual intimate imagery (NCII) of real 10
individuals.vi 11
The rapid development of foundation models poses significant challenges to understanding 12
their capabilities and misuse risks,2 and this document provides a basis to identify, measure, 13
and mitigate these risks across the AI lifecycle. Misuse risks are not a function of the model 14
alone—they result in part from malicious actors’ motivations, resources, and constraints, as 15
well as the ways that models are integrated into applications and society’s defensive measures 16
against harms.3 As a result, the guidelines provided here address both technical and broader 17
societal aspects of these risks.  18
This document identifies procedures and outlines a framework to anticipate, measure, and 19
mitigate misuse risks from foundation models, as well as suggests how organizations can 20
provide transparency into risk management practices. This document focuses particularly on 21
foundation models’ initial developers, but additional actors across the AI supply chain play a 22
role in managing misuse risks, which Section 3 describes in greater detail. 23

i This term, and other terms throughout the document, are defined in Appendix A.
ii Executive Order 14110 defines a “dual-use foundation model” as “an AI model that is trained on broad data;
generally uses self-supervision; contains at least tens of billions of parameters; is applicable across a wide range of
contexts; and that exhibits, or could be easily modified to exhibit, high levels of performance at tasks that pose a
serious risk to security, national economic security, national public health or safety, or any combination of those
matters, such as by: (i) substantially lowering the barrier of entry for non-experts to design, synthesize, acquire, or
use chemical, biological, radiological, or nuclear (CBRN) weapons; (ii) enabling powerful offensive cyber operations
through automated vulnerability discovery and exploitation against a wide range of potential targets of cyber-
attacks; or (iii) permitting the evasion of human control or oversight through means of deception or obfuscation.”
iii As codified in 14 U.S.C. § 278h-1.
iv Section 4.1(a)(ii) of Executive Order 14110 directs the Secretary of Commerce to “Establish appropriate
guidelines (except for AI used as a component of a national security system), including appropriate procedures and
processes, to enable developers of AI, especially of dual-use foundation models, to conduct AI red-teaming tests to
enable deployment of safe, secure, and trustworthy systems. These efforts shall include: (A) coordinating or
developing guidelines related to assessing and managing the safety, security, and trustworthiness of dual-use
foundation models.”
v Section 3.3(e)(ii) of the Memorandum tasks the AI Safety Institute to “issue guidance for AI developers on how to
test, evaluate, and manage risks to safety, security, and trustworthiness arising from dual-use foundation
models...,” including on a range of subtopics in scope here.
vi Appendix D provides considerations for chemical and biological misuse risks; Appendix E for cyber misuse risks.

<!-- page 6 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

1

2. SCOPE 1
Risks. This document focuses on misuse risk from dual-use foundation models. Consistent with 2
Section 3(k) of Executive Order 14110,4 this includes foundation models that exhibit, or could 3
be easily modified to exhibit, high levels of performance at tasks that can pose a serious risk to 4
security, economic security, public health or safety, or any combination of those matters 5
(hereafter referred to jointly as ‘public safety’). This document addresses both potential future 6
misuse harms, such as a foundation model facilitating the development of a biological or 7
chemical weapon, as well as current harms from misuse, such as a foundation model generating 8
CSAM or NCII. This document applies to the additional or novel misuse risk that a model 9
introduces (i.e., the marginal risk).5 10
This document does not address all important risks from foundation models, nor does it 11
address all risks to public safety that may arise from AI models that are not foundation 12
models.vii Actors across the AI value chain and throughout the AI lifecycle should manage these 13
additional risks as well, which may be consistent with relevant aspects of these guidelines, as 14
well as those provided in other guidance such as the Blueprint for an AI Bill of Rights6 and the 15
NIST AI 100-1 AI Risk Management Framework (AI RMF) and NIST AI 600-1 RMF Generative AI 16
Profile (AI RMF Generative AI Profile).7 17
Actors. The practices in this document principally focus on the role that the initial developers of 18
foundation models play in the AI lifecycle. Implementation of the key practices in this 19
document may vary depending on the size and resources of the developer. Initial developers 20
have the most insight into model design characteristics, development process, and baseline 21
capabilities. They can also take steps early in the development process to reduce a model’s risks 22
throughout its lifecycle, including across a range of downstream applications. Initial developers 23
also have control over how the model is initially made available to others, but in many cases, 24
they may share responsibility with downstream actors. Additional actors include cloud service 25
providers, model hosting platforms, downstream model adapters, application developers, 26
deployers, distribution platforms, third-party evaluators, and more.8 Section 3 provides 27
additional actors with examples of their roles in managing misuse risk.  28

vii For instance, many smaller, domain-specific models can also be misused in harmful ways. This document also
does not cover risks from accidental AI harms to public safety.

<!-- page 7 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

2

3. MISUSE RISK MANAGEMENT THROUGHOUT THE AI SUPPLY CHAIN 1
While not the primary focus of this document, actors across the AI supply chain have a role in 2
managing misuse risk in addition to developers. These actors include cloud service providers, 3
model hosting platforms, downstream model adapters, application developers, deployers, 4
distribution platforms, third-party evaluators and auditors, academic institutions, and 5
government agencies.9   6
These actors should implement appropriate processes and risk mitigations to help manage 7
misuse risk, such as the relevant guidelines outlined in Section 5 of this document and other 8
NIST guidance, including the AI RMF and its Generative AI Profile. Actors should also collaborate 9
to understand and mitigate misuse risks along the AI supply chain and throughout the AI 10
lifecycle, such as the information sharing recommendations outlined in Objective 7 in Section 5. 11
While best practices for managing misuse risk continue to evolve, this section outlines steps 12
that these actors can take to manage and mitigate misuse risk specific to their roles in the AI 13
supply chain, including: 14
1. Compute providers: Actors that provide compute infrastructure to foundation model 15
developers and deployers, such as cloud service providers, can implement physical and 16
cybersecurity practices to protect model weights and other sensitive model elements, as 17
well as engage with developers to ensure such practices are proportionate to misuse 18
risk. Objective 3 in Section 5 provides specific guidelines that may be relevant to cloud 19
service providers. 20
2. Model hosting platforms: Actors that distribute and enable discovery of foundation 21
models and datasets used to build foundation models can adopt terms of service that 22
reduce misuse risks and implement systems for monitoring and reporting evidence of 23
misuse to support enforcement. Objectives 6 and 7 in Section 5 provide related 24
recommended practices.  25
3. Downstream model adapters, application developers, and deployers: AI systems may 26
inherit misuse risks from upstream foundation models. Design decisions made by 27
downstream actors when adapting models and integrating them into applications, such 28
as when implementing safeguards, as well as selection of deployment context and use 29
case, can impact misuse risk. To manage deployment-specific misuse risks, these actors 30
can use information shared from the initial developer as a starting point for managing 31
misuse risk and review all of Section 5, if necessary, with particular attention to 32
Objectives 5 and 6.  33
4. Distribution platforms: App stores and other platforms that enable the discovery, 34
distribution, and use of AI applications can define terms of service that reduce misuse 35
risks, apply system-level safeguards to models that are directly available for inference, 36
and implement systems for monitoring and reporting evidence of misuse to support 37
enforcement. Third-party platforms that do not directly host foundation models or AI 38
applications may host model outputs and thus be a potential source of misuse. These 39

<!-- page 8 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

3

platforms can also share information across the AI supply chain to help manage misuse 1
risk, as outlined in Objectives 6 and 7 in Section 5.  2
5. Third-party evaluators and auditors: Third parties can provide information and 3
knowledge related to public safety risks of foundation models to complement 4
developer-led misuse risk management. Fostering a community of third-party evaluators 5
and auditors helps maintain accountability for model developers and increases 6
institutional transparency around misuse risk management practices. Third-party 7
evaluators and auditors can help define standards for misuse risk management practices 8
and formalize processes for reliable audits and evaluations of foundation models.10 They 9
can also help improve misuse risk management practices overall, such as by developing 10
methods to incorporate empirical evidence of real-world harm into misuse risk 11
assessments. To perform evaluations, third parties can review the documentation 12
provisions throughout Section 5, with particular attention to Objectives 1, 4, 5, and 6. 13
6. Academics and external researchers: Academics and independent external researchers 14
can help advance scientific research related to AI safety and security practices, including 15
the development of novel model safeguards, methods and tools to measure misuse risk, 16
and innovative risk management practices. Academics and external researchers can also 17
consider how their research might contribute to implementation of the practices in 18
Section 5, with particular attention to Objectives 1, 4, and 5.  19
7. Government agencies: Government agencies can coordinate national security efforts to 20
understand sensitive misuse risks in classified settings and enforce federal, civil, and 21
criminal law to combat misuse. Government agencies can complement other actors in 22
disseminating information about misuse risk, work with partners across the AI supply 23
chain to develop practices for assessing misuse risk, and foster a robust ecosystem of 24
third-party evaluator and auditors. Government agencies can also take steps to improve 25
societal capacity and resilience to increase robustness to the possible misuse of 26
foundation models.  27
8. Users and the public: The public can report observed misuse incidents to law 28
enforcement, incident databases, and actors across the AI supply chain. Users can 29
report information, such as model issues that may lead to misuse risk (hereafter 30
referred to as ‘model flaws’), to actors across the AI supply chain.  31

<!-- page 9 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

4

4. KEY CHALLENGES IN MANAGING MISUSE RISKS 1
While this document provides guidelines for managing misuse risks of foundation models, it is 2
important to acknowledge that these approaches are still nascent, posing both methodological 3
and scientific challenges to implementation. For instance, best practices for evaluating model 4
capabilities, identifying and accurately measuring potential misuse risks, and monitoring real-5
world misuse remain in flux. Organizations should collaborate and take appropriate steps to 6
build an empirical basis to evaluate and mitigate misuse risks. Such challenges include: 7
1. Foundation models are general purpose. Models trained on a broad data distribution 8
can often be applied across many different domains and integrated into a variety of 9
downstream systems, including domains and systems not expressly considered by the 10
developer. This flexibility renders anticipating the potential ways in which a model might 11
be misused difficult and complicates the measurement and monitoring of misuse risk.  12
2. Models are only one element of misuse risk. Misuse risk is not simply a function of 13
model capabilities identified in specific evaluations. Public safety harms often arise from 14
the successful completion of a chain of tasks, where only a subset benefit from model 15
capabilities. While models can provide new methods to enact harm, enhance actors’ 16
abilities to commit existing harms, or increase the number of actors that can participate 17
in malicious activity, harms to public safety also often require physical infrastructure, 18
distribution mechanisms, or complex interactions in the physical world.11 Bad actors 19
may also already have access to existing tools that serve their needs better than 20
foundation models, and existing methods to prevent harm—such as controls on physical 21
dual-use materials—may be substantially more determinative of real-world risks.12 22
3. Model capabilities that relate to misuse risk are difficult to predict. It is difficult to 23
predict the model capabilities that may increase the risk of misuse. In many instances, 24
increasing the amount or quality of a foundation model’s training data, the quantity of 25
compute used to build or run the model, or the number of parameters in the model can 26
improve its performance.13 However, these factors, while useful heuristics in some 27
instances, have limited precision and an uncertain relationship to a model’s capabilities 28
and potential misuse risks.14  29
4. It is difficult to accurately emulate threat actors and simulate misuse scenarios. 30
Assessing misuse risk requires understanding how a malicious actor might in practice 31
exploit a foundation model’s capabilities or circumvent safeguards to cause harm. 32
Organizations may not have the capacity to accurately simulate the resources, time, or 33
access to infrastructure or niche expertise available to a malicious actor. Realistic 34
emulation of malicious actors may also be prohibitively dangerous or unethical, such as 35
attempting to develop a volatile substance, generate non-consensual intimate imagery, 36
or harm real people. 37
5. Results from misuse risk measurement may not generalize to real-world situations. 38
Model performance on one task may not provide reliable evidence of its performance 39
on others, even when the two tasks appear related.15 For instance, initial benchmarks 40

<!-- page 10 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

5

that are cheaper and easier to carry out may suggest a model has dangerous 1
capabilities, but this concern may not be substantiated when the model is tested in 2
more rigorous and realistic conditions. 3
6. Evaluating misuse risk may require scarce domain expertise. Information about some 4
risks, like the potential for a foundation model to enable a malicious actor to develop a 5
chemical or biological weapon, may be closely guarded. Organizations developing 6
foundation models may not have the domain expertise – or access to the expertise – 7
necessary to assess or manage some misuse risks. 8
7. Safeguards to protect against misuse are often brittle, and methods to evaluate their 9
efficacy are nascent. Foundation model developers can implement safeguards to 10
protect their models from misuse, such as those included in Appendix B, but few 11
techniques exist to evaluate the adequacy of those safeguards under real-world 12
conditions. Safeguards are often underdeveloped and brittle: for example, foundation 13
models trained to decline harmful requests will often comply with those requests if an 14
adversary reframes them or adds additional text to the prompt.16 15

<!-- page 11 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

6

5. OBJECTIVES AND PRACTICES TO MANAGE MISUSE RISKS 1
This section outlines seven objectives that organizations should aim to meet to assess and 2
manage the risk that their foundation models will be misused to deliberately harm public 3
safety.viii This document also provides practices and recommendations for each objective as 4
non-exhaustive examples of how organizations can meet the objectives in a manner they deem 5
appropriate and proportionate to the risks posed by their foundation models.  6
These objectives are: 7
1. Identify potential misuse risk 8
2. Plan to manage misuse risk 9
3. Protect the model from unauthorized access (if necessary) 10
4. Measure misuse risk associated with model deployments  11
5. Mitigate misuse risk before deployments  12
6. Monitor and respond to misuse  13
7. Disclose misuse risk management practices 14
Managing misuse risk is an iterative process, and organizations should consider all seven 15
objectives holistically to manage foundation model misuse risks. Organizations should also 16
adopt additional risk management measures and communicate with other actors in the AI 17
supply chain, where and when appropriate. However, implementing these practices cannot 18
guarantee that actors will not misuse a foundation model, and model developers should remain 19
aware of possible misuse risks. For instance, organizations can consider these objectives in 20
conjunction with existing NIST guidance, particularly the NIST AI RMF and its Generative AI 21
Profile, and NIST SP 800-30 Guide for Conducting Risk Assessments. See Figure 1 for primary 22
correspondence of objectives across the AI lifecycle. 23

viii In some cases, the objectives may be difficult to fully achieve based on the state of the science. In such cases,
and depending on model capabilities, the practices and recommendations may serve primarily to help further
advance towards the objective rather than ensuring it would be fully achieved.

<!-- page 12 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

7

 1
Figure 1. NIST AI 800-1 Objectives in the AI Lifecycle. The two inner circles display the objectives included in Section 2
5 and the outer circle indicates their primary corresponding stages in the AI lifecycle.17 Plan, Protect, and Disclose 3
(Objectives 2, 3, and 7, respectively) may be applicable across all AI lifecycle stages. Note that these objectives 4
should be implemented holistically and iterated upon as necessary across the AI lifecycle to manage misuse risk 5
particular to a specific foundation model. 6
The specific elements of each objective below include:  7
1. Objective: a target outcome that will help organizations manage misuse risks. 8
2. Practice: a suggested practice that can help organizations achieve an objective. This 9
document proposes practices that may not be appropriate for all contexts. Alternative 10
practices may also achieve these objectives, and new practices are likely to be 11
developed over time.  12
3. Recommendation: an implementation characteristic or consideration that is often 13
important for a practice to effectively achieve an objective. These recommendations 14
may not be appropriate in all cases and in some cases will not be exhaustive of the 15
measures necessary for a practice to help achieve an objective.  16
4. Documentation: examples of information that could demonstrate whether and how a 17
practice was implemented, as well as potential evidence of its effectiveness and 18
comprehensiveness for internal record-keeping or external information sharing. Sharing 19
documentation with the public and/or select parties can help demonstrate 20
implementation, facilitate collaboration across the AI supply chain, and develop shared 21
best practices for managing misuse risks. If an organization relies on alternative 22
practices to achieve an objective, a similar level of documentation and a rationale for 23
why the alternative practices match or exceed the efficacy of provided practices can be 24
used. In situations where documentation details are sensitive, an organization may need 25

<!-- page 13 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

8

to calibrate the amount and type of information shared externally, such as only sharing 1
with appropriate national security authorities. 2
 3
Objective 1: Identify potential misuse risk 4
Anticipate the possible ways in which malicious actors might use the model to cause harm 5
(hereafter referred to as ‘threat profiles’) and assess the potential impact of this harm before 6
the model is developed. 7
Practice 1.1: Anticipate model capabilities. 8
Forecast potential model capabilities that may present misuse risk by surveying evidence from 9
deployed models with similar capabilities to the model (hereafter referred to as ‘proxy models’).  10
Recommendations for Practice 1.1: 11
1. Prioritize evidence from widely deployed and studied proxy models. 12
2. Consider also collecting evidence from less similar models, such as those that are 13
significantly more or less powerful than the model (e.g., if a less capable model 14
presents a misuse risk, prioritize measuring for that risk). 15
3. Consider other factors beyond model characteristics, such as resources available to 16
develop the model, when relating the proxy models’ capabilities to anticipated ones. 17
4. Collect information about the prevalence of misuse, the usefulness of proxy models for 18
potentially harmful or dual-use real-world tasks, and the efficacy of safeguards. 19
5. Assess the degree of uncertainty in these estimates based on the difference between 20
the proxy model and the planned model, how those differences are expected to affect 21
their capabilities, and the reliability and completeness of the evaluations available for 22
proxy models.  23
6. Consider involving experts in anticipating model capabilities, such as by potentially 24
granting them access to intermediate model checkpoints for open-ended 25
experimentation to identify other ways the model could be misused to cause harm. 26
7. If capability forecasts are uncertain and include the possibility that the model may 27
require increased risk mitigations, consider increasing the frequency of capability 28
measurements during the development process (Objective 4) and expanding the 29
organization’s planned risk mitigation measures (Objective 5).  30
Documentation for Practice 1.1: 31
a. The proxy model(s) used for comparison and the specific capabilities that relate to 32
misuse risk.  33
b. The anticipated difference between the model’s forecasted capabilities and the 34
capabilities of the proxy model(s). 35

<!-- page 14 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

9

Practice 1.2 Create threat profiles.   1
Before training a model, identify and maintain a list of threat profiles based on the anticipated 2
model capabilities.  3
Recommendations for Practice 1.2: 4
1. Identify (i) the threat actor or actors that may misuse the model, (ii) the chain of tasks 5
required to realize harm, (iii) the relevance of model capabilities to each task, and (iv) 6
the harm(s) that the model could help the threat actor(s) enact. 7
2. Incorporate relevant information about possible misuse identified from proxy models in 8
Practice 1.1. Examples of possible misuse risks may include the risk that a model may 9
lower the barriers to the design, development, distribution, or use of chemical, 10
biological, radiological, or nuclear (CBRN) weapons or the automation of an offensive 11
cyberattack. 12
3. Use real data, case studies, or expert opinions to inform threat profiles and help identify 13
gaps.ix  14
4. Develop a plan for identifying and adding threat profiles to this list as future research 15
reveals new potential or ongoing misuse risks (Objective 2).  16
Documentation for Practice 1.2: 17
a. A list of identified threat profiles.  18
b. A description of how these threat profiles were selected and judged to have adequate 19
coverage. 20
c. A plan for updating this list as new misuse risks may materialize. 21
Practice 1.3: Conduct risk assessments.  22
For each threat profile, assess the potential misuse risk by estimating the likelihood of harm 23
occurring and the impact if that harm occurred.  24
Recommendations for Practice 1.3: 25
1. Consider both quantitative and qualitative assessments of likelihood and impact, if 26
possible.  27
2. Account for alternative tools already available to threat actors, such as existing models 28
or other digital tools, and assess the model’s marginal risk of misuse relative to that 29
baseline.18 30

ix Consider that there may be multiple threat profiles for a given capability; for example, automation of
vulnerability discovery might be used in different ways by a criminal organization or by a nation state,
corresponding to distinct threat profiles.

<!-- page 15 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

10

3. Consider the new risk the model may introduce, such as the model’s ability to help an 1
actor increase the scale, prevalence, or frequency, decrease the cost, or improve the 2
effectiveness or efficiency of their malicious activity.    3
4. Consider malicious actors’ potential motivations, willingness, and capacity to enact 4
harm, as well as the number of malicious actors that may exist.19 5
5. Account for existing mitigations and barriers, such as limitations on access to physical 6
resources needed to enact harm, and the level of societal preparedness to defend 7
against that harm.  8
6. Use information about the real-world impact and use of proxy models to inform the 9
assessment; update these assessments as new information about real-world impact 10
materializes. 11
7. Update estimates if changes in the broader ecosystem either increase or decrease 12
vulnerability to potential harms. 13
8. Recognize areas of uncertainty and sensitivity and account for these areas when 14
communicating and using impact assessments.   15
Documentation for 1.3: 16
a. A risk assessment for each identified threat profile.  17
b. A comparison between past risk assessment predictions and actual model impact for 18
proxy models, when and if relevant and accessible. 19
 20
Objective 2: Plan to manage misuse risk 21
Determine a strategy to apply appropriate risk mitigations for each potential model capability 22
that may introduce misuse risk. Align development and deployment plans with the resources, 23
time, and operational constraints that may be required to manage potential misuse risk.  24
Practice 2.1. Map anticipated model capabilities to appropriate risk mitigations 25
to manage misuse risk.  26
For foundation models with capabilities that may introduce misuse risks, identify the risk 27
mitigations necessary to manage the risks that might arise from these particular capabilities 28
across the AI lifecycle. Appendix B includes a list of example risk mitigations. 29
Recommendations for Practice 2.1: 30
1. Consider the costs and benefits of planned risk mitigations, using both qualitative and 31
quantitative comparisons. 32
2. Consider the risk in the context of organizational risk tolerances, which may reflect legal 33
and regulatory obligations.  34
3. Identify and articulate evidence to justify the adequacy of planned risk mitigations.  35

<!-- page 16 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

11

4. Refine planned methods to mitigate misuse risk periodically based on adjustments to 1
identified threat profiles, changes in factors that affect risk tolerance (such as increases 2
in expected benefits), and information about real-world performance. 3
5. As measurement and real-world monitoring is performed, continue to re-assess the 4
safeguards necessary to manage misuse risk for each particular capability.  5
Documentation for Practice 2.1: 6
a. The procedure and criteria used to define risk mitigations proportionate to model 7
capabilities. 8
b. An articulation of the adequacy of these mitigations to manage misuse risk. 9
Practice 2.2 Establish an organizational plan to manage misuse risk.   10
Develop and implement an organizational plan, including the expected resources needed and 11
timelines to manage misuse risk throughout the AI lifecycle, including iterations and 12
improvements to the model. 13
Recommendations for Practice 2.2: 14
1. Plan for information security and physical security practices necessary to manage 15
misuse risk, when appropriate.  16
2. Plan research needed to implement and evaluate adequate safeguards. If necessary, 17
base these plans on the mapping established in Practice 2.1. 18
3. Plan for decision-making about model deployment. This plan should include the 19
organization’s plan for pre-deployment testing and determining which appropriate risk 20
mitigations are available.  21
4. Plan to monitor evidence of real-world misuse and potential risk. Develop processes for 22
adjusting these organizational plans, as well as deployment or development approaches, 23
as necessary. 24
5. Consider consulting existing resources for developing and implementing such 25
organizational plans, such as the NIST RMF and other guidance.20 26
Documentation for Practice 2.2: 27
a. The planned risk mitigations, accounting for technical and resource constraints. 28
b. Concrete steps to take if subsequent measurements suggest mitigations are not 29
adequate to manage misuse risk.  30
c. Plans to update (a) and (b) as necessary.  31
 32
 33
 34

<!-- page 17 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

12

 1
Objective 3: Protect the model from unauthorized access (if 2
necessary) 3
Some models may pose particular misuse risk, warranting careful storage. In such cases, take 4
steps to assess and prevent the risk that entities and individuals not authorized by the developer 5
will access the model, its associated weights, or other information that could facilitate re-6
creation of the model in an unauthorized manner (hereafter referred to as ‘unauthorized 7
access’).x  8
Practice 3.1: Assess misuse risk from threat actors gaining unauthorized access 9
to the model. 10
Based on threat profiles and risk assessments identified in Objective 1, assess whether 11
unauthorized access to a model may pose or significantly increase misuse risk, and if so, 12
estimate that risk. 13
Recommendations for Practice 3.1: 14
1. Consider possible threat actors’ motivations and level of sophistication related to 15
gaining unauthorized access to the model.21 16
2. Consider the organization’s compliance with applicable cybersecurity best practices, 17
such as NIST Special Publication 800-53 and Secure Software Development Framework 18
(SSDF), to help assess the probability of unauthorized access.22 19
3. Consider the threat posed by insiders, such as an individual involved in developing or 20
deploying the model who may behave maliciously or collaborate with an external 21
attacker. 22
4. When relevant, consider using cybersecurity red teams and penetration testing to 23
assess how difficult it would be for an actor to circumvent security measures. 24
Documentation for Practice 3.1: 25
a. A summary of evidence collected to evaluate the risk of threat actors gaining 26
unauthorized access to the model, including the results of any cybersecurity red team 27
exercises and penetration testing.  28
Practice 3.2: Maintain security practices sufficient to prevent unauthorized 29
access. 30

x In this document, unauthorized access generally refers to an intrusion or breach of an information system or
asset that the accessing entity has not been granted any access to (a full definition is provided in Appendix A). This
is differentiated from unauthorized use, which here refers to an entity misusing technical access that they have
been granted legitimately to carry out some unauthorized purpose, such as by jailbreaking a model or violating its
terms of service.

<!-- page 18 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

13

Implement security practices, to the extent possible, commensurate with risk to protect against 1
threat actors gaining unauthorized access to the model.  2
Recommendations for Practice 3.2: 3
1. Consider adopting existing U.S. government cybersecurity guidance and applicable 4
international or industry standards.23 5
2. Apply security practices tailored to the context of foundation models, such as 6
protections against exfiltrating large amounts of data (e.g., model weights) and other 7
vulnerabilities (e.g., extraction attacks).24 8
3. Apply appropriate protections against insider threats, such as limiting access to model 9
weights within the organization or implementing two-party control systems. 10
4. Re-assess the risk of unauthorized access as security practices are implemented. 11
5. Only develop a model that relies on confidentiality to manage misuse risk when the risk 12
of threat actors gaining unauthorized access to the model is sufficiently mitigated. 13
When the organization is made aware of an increased risk of unauthorized access, 14
adjust or halt further development until the risk of unauthorized access is adequately 15
managed. 16
Documentation for Practice 3.2: 17
a. A summary of security measures that have been implemented to reduce the risk of 18
threat actors gaining unauthorized access to the model. Consider including references to 19
standards used to implement such security measures.  20
 21
Objective 4: Measure misuse risk associated with model deployments 22
Measure model capabilities related to identified misuse to help quantify risk. Rely on methods 23
that incorporate both technical and societal factors and prioritize accuracy while avoiding harm 24
from measuring dangerous activities. 25
Practice 4.1: Evaluate model capabilities on tasks relevant to assessing misuse 26
risk.   27
Conduct pre-deployment evaluations of the model to measure performance on specific 28
capabilities that may introduce misuse risk identified in Practice 1.3. Appendix C lists possible 29
characteristics of methods to measure misuse risk. 30
Recommendations for Practice 4.1: 31
1. Evaluate the model’s capabilities throughout the development process: during training, 32
after training, and when integrated into a downstream system or interface.  33
2. Consider using automated or otherwise less expensive tests on tasks related to real-34
world harm to indicate that a model lacks dangerous capabilities. If initial tests are 35

<!-- page 19 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

14

inconclusive or indicate a potential risk, conduct more costly and precise 1
measurements.  2
3. Consult relevant experts when creating evaluations to ensure that they are indicative of 3
real-world scenarios. 4
4. Maximize model performance on evaluation tasks by adjusting prompts, software 5
scaffolding, fine-tuning the model, or other means. 6
5. If a gap exists between the effort or resources applied by evaluators to maximize system 7
performance and the resources that could be applied by a threat actor, account for that 8
gap when interpreting evaluation results.  9
6. Avoid overlap between data used to train a model and data used in capability 10
evaluations and measure the extent of any overlap.  11
7. Account for the relative immaturity of some measurement approaches and consider 12
misuse risk in the context of this immaturity. Update evaluations accordingly as the 13
state of science advances. 14
8. Compare measurements to real-world observations of proxy models identified in 15
Practice 1.1 to help calibrate the relationship between real-world observations and 16
controlled model evaluations. If sufficient proxy models have been deployed but 17
information about real-world performance is not available, consider conducting 18
additional relevant measurements of performance on harmful or dual-use tasks in a 19
realistic setting. 20
Documentation for Practice 4.1: 21
a. A list of tasks that were used to evaluate each threat profile, results of these tests, and a 22
representative subset of datasets used for each evaluation. 23
b. A methodological description for each evaluation in enough detail to reproduce it. For 24
example, outline methods for data collection, preprocessing, prompts, inference 25
parameters, and evaluator models. 26
c. An analysis of the relationship between evaluation tasks, assessed capabilities, and 27
potential misuse risks identified in Objective 1 that addresses uncertainties and 28
limitations. 29
Practice 4.2: Red-team safeguards. 30
Use red-teaming to assess whether threat actors could bypass model or system safeguards 31
designed to prevent misuse.  32
Recommendations for Practice 4.2: 33
1. Evaluate whether an adequately resourced red team can misuse the model to achieve a 34
predetermined goal or accomplish a related proxy task in a realistic deployment context. 35
If using proxy tasks, ensure that they are at least as easy to achieve as undesirable real-36

<!-- page 20 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

15

world outcomes, considering both the inherent complexity of the task and any 1
additional difficulty introduced by safeguards. 2
2. Assemble red teams based on their ability to succeed at the determined task, 3
considering factors such as relevant domain expertise, their independence from the 4
model developer, diversity of perspectives, and lack of incentives that conflict with their 5
red-teaming goal. 6
3. Provide the red team with a clearly defined task. Determine a performance metric for 7
measuring the red team’s success and provide incentives and accountability for task 8
completion.  9
4. Compare the red team’s expertise, resources, and time available to those of a relevant 10
threat actor. Ensure that the red team is adequately resourced to the extent possible 11
and consider providing alternative and/or additional resources to the red team or 12
making the red team’s task easier in other ways (such as providing additional access to 13
the model or dividing complex tasks into constituent pieces) to compensate for any 14
remaining gaps between the red team and threat actors.25 15
5. Provide the red team with at least as much information about the model (or 16
downstream system if testing at the integration level) as would be available to an 17
attacker and make explicit any respects in which the red team lacks full information 18
about the design of safeguards. 19
6. Attempt to minimize institutional or legal obstacles to red teams succeeding at their 20
tasks. Consider providing appropriate protections, such as waiving terms of service and 21
legal liability. 22
7. Consider each level of access to a model that a threat actor might have, ranging from 23
limited access through an API to direct access to the code and parameters that define 24
the model, and determine the minimum level of access (if any) that allows the red team 25
to accomplish its goal. 26
8. Consider testing the model at different levels, such as the model without safeguards, 27
the model with safeguards, and the model integrated into a downstream system or 28
interface. 29
9. Consider information that may become public about how to circumvent safeguards 30
when assessing risk, including when information will be disclosed to the developer 31
relative to the public and the technical feasibility of rapidly addressing disclosed model 32
flaws. 33
Documentation for Practice 4.2: 34
a. For each red team exercise, a description of the risks it is intended to address, the goal 35
provided to the red team, the composition and expertise of the red team, and the 36
resources, level of access, and time available to the red team.  37

<!-- page 21 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

16

b. A high-level summary of the results of red-teaming, including the level of success 1
achieved by the red team at their task, feedback from the red team about their 2
interpretation of the outcome, and any other relevant red-teaming characteristics.  3
 4
Objective 5: Mitigate misuse risk before deployments 5
Make deployment decisions based on available safeguards and their efficacy to adequately 6
mitigate misuse risks, based on plans determined in Objective 2. Appendix B outlines a list of 7
example methods to mitigate misuse risk. 8
Practice 5.1: Implement safeguards proportionate to the model’s misuse risk. 9
Implement safeguards designed to prevent the model from being misused, as identified in 10
Practice 2.1.  11
Recommendations for Practice 5.1: 12
1. Establish evidence of safeguards’ effectiveness before relying on them to prevent 13
misuse risks, such as by red-teaming (Practice 4.2) and monitoring the efficacy of 14
safeguards for proxy models (Practice 1.1).  15
2. Consider implementing safeguards at various stages of model development, such as 16
before, during, and after training and once the model has been integrated into a 17
downstream system, as well as other mitigation measures. Some examples are included 18
in Appendix B.  19
Documentation for Practice 5.1: 20
a. The list of safeguards that have been implemented. 21
b. A summary of any evidence available about the safeguards’ efficacy, which may include 22
the result of safeguard evaluations via red teams and other testing. 23
Practice 5.2: Assess misuse risk based on implemented safeguards. 24
Evaluate misuse risk in the context of implemented safeguards to assess the remaining ‘residual 25
risk.’ Use this assessment to inform the choice of deployment strategy.  26
Recommendations for Practice 5.2: 27
1. Identify planned deployments that could impact misuse risk. For example, consider 28
whether the planned deployment could impact the number of actors who have access 29
to a model or the level of access that they would have. 30
2. Estimate misuse risk based on appropriate measurements conducted under Objective 4 31
and comparisons to proxy models conducted in Practice 1.1. 32
3. If additional safeguards are added in response to identified risks, consider re-assessing 33
misuse risk prior to deployment by carrying out red-teaming exercises (Practice 4.2) 34
with the additional safeguards in place. 35

<!-- page 22 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

17

Documentation for Practice 5.2: 1
a. The level of model access provided for each deployment. 2
b. The assessed misuse risks associated with each deployment.  3
Practice 5.3: Adopt appropriate deployment strategies based on misuse risk 4
assessments. 5
If risk cannot be adequately managed after completing Practice 5.1 and 5.2, determine whether 6
the deployment should be modified or delayed. 7
Recommendations for Practice 5.3: 8
1. Assess residual risk by incorporating the overall assessed misuse risk from the selected 9
deployment strategy and mitigations from implemented safeguards. 10
2. Consider deployment strategies that provide additional real-world evidence to inform 11
risk assessments without presenting significant misuse risks. 12
3. Consider whether additional safeguards are feasible to implement prior to deployment, 13
whether additional time could be used to carry out a more reliable estimate of risk, or 14
whether a more limited deployment may be more appropriate given the level of 15
assessed risk.  16
4. Consider leaving a buffer between the estimated level of risk—given the implemented 17
safeguards and the deployment strategy—and the associated anticipated real-world risk 18
(hereafter referred to as a ‘margin of safety’). This margin of safety could incorporate 19
how threat actors may continue to acquire new knowledge about how to misuse or 20
augment the model after it is deployed26 and how to circumvent safeguards.27 Consider 21
a larger margin of safety to manage risks that are more severe or less certain.  22
Documentation for Practice 5.3: 23
a. The basis for determining that the risk of misuse was adequately managed for a 24
deployment decision, including that the deployment’s risks were within the 25
organization’s risk tolerances.  26
 27
Objective 6: Monitor and respond to misuse 28
Collect information about model usage to improve understanding of misuse risk, adapt to 29
emerging risks, and improve future deployments. Engage with and encourage findings from the 30
public, civil society organizations, external researchers, and the foundation model’s distribution 31
partners. 32
Practice 6.1: Monitor for evidence of misuse.  33
Accounting for differences in deployment strategies; develop and implement a plan for 34
monitoring model deployments for misuse. 35

<!-- page 23 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

18

Recommendations for Practice 6.1: 1
1. Monitor APIs, model hosting platforms, and other distribution channels for misuse while 2
maintaining privacy of users. 3
2. Build or procure systems to enable automated detection of misuse.  4
3. Periodically assess the effectiveness of misuse detection systems, including through red-5
teaming.   6
4. Request that distribution channels monitor for misuse and share information regarding 7
this monitoring.   8
5. Consider tiered methods of detection, such as scanning for misuse using less costly 9
automated methods and then validating through direct human intervention, to help 10
prioritize limited resources, improve privacy, and increase coverage.  11
6. Collaborate with other actors, such as content distribution platforms, downstream 12
model adapters, cloud service providers, third-party researchers, and law enforcement 13
officials, to track real-world incidents of misuse.  14
Documentation for Practice 6.1: 15
a. A summary of the mechanisms used to monitor each distribution channel for a 16
foundation model and the methods for determining the effectiveness of those 17
mechanisms.  18
Practice 6.2: Respond to incidents of model misuse.  19
Develop incident response processes to manage real-world misuse after model deployments. 20
Recommendations for Practice 6.2: 21
1. Establish clear organizational responsibilities for accountable incident response 22
processes.  23
2. Plan for responses to plausible novel scenarios of misuse, such as strengthening 24
safeguards or implementing new ones.28 25
3. Plan for how identified instances of misuse will inform future development and 26
deployment decisions, especially when reducing access to the model may not be 27
possible. 28
4. Consider carrying out drills to practice responding to time-sensitive and safety-critical 29
scenarios of misuse, if appropriate given the level of risk of the deployment. 30
Documentation for Practice 6.2: 31
a. A summary of the incident response process and the organizational roles and 32
responsibilities in the process. 33
Practice 6.3: Establish misuse reporting mechanisms. 34

<!-- page 24 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

19

Establish channels and protections for reporting known instances of misuse and issues that 1
could lead to misuse risk. 2
Recommendations for Practice 6.3: 3
1. Adopt policies that protect and reward individuals who report model issues related to 4
misuse risk.  5
2. Establish formal processes to adjudicate concerns from the public, employees, and 6
contractors in a timely fashion.  7
3. Communicate the identified issues or misuse instances clearly with employees and 8
contractors, as appropriate. 9
Documentation for Practice 6.3: 10
a. A summary of the organization’s policies with respect to internal and external reporting 11
of misuse and issues that could lead to misuse.  12
b. For internal use, a summary of possible limitations of evaluations or safeguards relevant 13
to risk assessments, possible deficiencies within the organization’s risk management 14
processes, and any detected errors in disclosures related to misuse risk. 15
Practice 6.4: Provide safe harbors for third-party safety research.  16
Create protections for third-party researchers to encourage research on reducing misuse risk. 17
 Recommendations for Practice 6.4: 18
1. Publish a clear vulnerability disclosure policy for model flaws that outlines how such 19
flaws should be shared with the developer and the public, and how the organization will 20
respond to reported flaws.29 21
2. Publish a clear safe harbor policy that commits to not pursuing legal action against or 22
restricting the accounts of external safety researchers that act in good faith and comply 23
with the vulnerability disclosure policy.30 24
3. Consider providing support and accommodations for vetted external researchers’ 25
interactions with the model, such as providing researchers with access to models with 26
fewer safeguards to conduct post-deployment red-teaming exercises. 27
Documentation for Practice 6.4: 28
a. A vulnerability disclosure policy. 29
b. A safe harbor policy.  30
c. A summary of the organization’s commitment to not pursue legal action against third-31
party researchers acting in good faith.  32
d. A description of the organization’s process for providing vetted researchers with access 33
to models with fewer safeguards.31 34

<!-- page 25 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

20

Practice 6.5: Create bounties for issues related to misuse risk. 1
Establish a bounty program to incentivize researchers to identify model flaws.  2
Recommendations for Practice 6.5: 3
1. Establish a program to incentivize researchers to find model flaws and disclose them 4
according to the vulnerability disclosure policy established in Practice 6.4.32  5
2. Consider referring to norms and best practices of existing bug bounty programs, such as 6
those instituted by software vendors, to guide program development. 7
Documentation for Practice 6.5: 8
a. The terms of the bounties and details regarding the process for submitting model flaws. 9
 10
Objective 7: Disclose misuse risk management practices 11
Provide transparency to the public and relevant entities about the organization’s processes for 12
addressing misuse risk to facilitate understanding, accountability, collaboration, and scientific 13
advancement. 14
Practice 7.1: Publish transparency reports. 15
Regularly publish transparency reports that include key details regarding misuse risks, how 16
those risks are assessed and managed, and roadmaps for safety and security improvements. 17
Recommendations for Practice 7.1: 18
1. Share the methodology and results of pre- and post-deployment evaluations of model 19
capabilities, risks, and mitigations, including as much detail about the data and 20
evaluation methodology as can be disclosed without introducing risks to public safety.33  21
2. Share details regarding the safeguards in place for the model, including how they are 22
applied across different distribution channels, with as much detail as can be shared 23
without rendering the safeguards ineffective.34  24
3. Share information about data used to build the model that is relevant to assessing the 25
misuse risk, such as criteria for data filtering, criteria for data selection, and data 26
sources, when possible.35  27
4. Share steps that downstream developers and deployers of AI systems that integrate the 28
foundation model should take to manage misuse risk.  29
5. Share relevant details about the internal organizational processes used to create risk 30
assessments and to make deployment and development decisions. 31
6. Make the transparency reports publicly available, update them on a regular basis (e.g., 32
with each new major version of the model), and include key information related to 33
misuse risk.36  34

<!-- page 26 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

21

7. Consider aligning transparency reports with existing public AI safety commitments, such 1
as those made to the White House Voluntary Commitments, the HAIP G7 Code of 2
Conduct, and the Seoul Frontier AI Safety Commitments.37  3
Documentation for Practice 7.1: 4
a. A public transparency report.   5
Practice 7.2: Disclose information about risk management practices. 6
Share detailed information on risk management practices with other developers, downstream 7
deployers, and other entities across the AI supply chain, as appropriate,xi to advance the science 8
of AI safety.  9
Recommendations for Practice 7.2: 10
1. Share information covering the practices used to achieve the objectives listed in this 11
document, including at least as much detail as described in the documentation sections 12
for each practice. 13
2. Share information about threat profiles with other entities across the AI supply chain 14
and the public to develop a joint knowledge base and save resources.   15
Documentation for Practice 7.2: 16
a. A summary of the list of stakeholders that receive information about risk management 17
practices and the types of information disclosed to them. 18
Practice 7.3: Report misuse incidents. 19
Based on existing best practices and an adequate consideration of the benefits and risks of 20
disclosing certain information, disclose incidents of misuse. 21
Recommendations for Practice 7.3: 22
1. Define the category of misuse events to report.38 23
2. Collate verified reports of misuse in a commonly used and standardized format.39   24
3. Share verified reports of misuse with relevant third parties, such as AI incident 25
databases and other model developers.40  26
Documentation for Practice 7.3: 27
a. A description of the incident reporting process, including an example of a type of 28
incident that might be reported and to whom it would be reported. 29

xi There may be some situations where sharing details of threat profiles widely is not appropriate, such as sharing
classified or highly sensitive information that is not widely known or disseminated. Consider the trade-offs
between information sharing risks due to the exposure of sensitive data and the benefits of transparency when
determining the recipient(s) and level of detail of documentation.

<!-- page 27 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

22

Appendix A. Glossary 1
Artificial Intelligence (AI) 2
A machine-based system that can, for a given set of human-defined objectives, make predictions, 3
recommendations, or decisions influencing real or virtual environments. Artificial intelligence systems use 4
machine- and human-based inputs to perceive real and virtual environments; abstract such perceptions into 5
models through analysis in an automated manner; and use model inference to formulate options for information 6
or action.41 7
AI Red-Teaming 8
A structured testing effort to find flaws and vulnerabilities in an AI system, often in a controlled environment and 9
in collaboration with developers of AI. AI red-teaming is most often performed by dedicated “red teams” that 10
adopt adversarial methods to identify flaws and vulnerabilities, such as harmful or discriminatory outputs from an 11
AI system, unforeseen or undesirable system behaviors, limitations, or potential risks associated with the misuse of 12
the system.42 13
Distribution Channel 14
The various ways in which a model could be distributed, including, but not limited to, public release of the model 15
weights, access to the model via an API supplied by a cloud service provider, access to the full model on open-16
source repositories, or access to a fine-tuned or otherwise augmented version of the model from a third-party 17
deployer. 18
Dual-Use Foundation Model or Foundation Model (for the purposes of these guidelines only)  19
An AI model that is trained on broad data; generally uses self-supervision; contains at least tens of billions of 20
parameters; is applicable across a wide range of contexts; and that exhibits, or could be easily modified to exhibit, 21
high levels of performance at tasks that pose a serious risk to security, national economic security, national public 22
health or safety, or any combination of those matters, such as by: substantially lowering the barrier of entry for 23
non-experts to design, synthesize, acquire, or use chemical, biological, radiological, or nuclear weapons; enabling 24
powerful offensive cyber operations through automated vulnerability discovery and exploitation against a wide 25
range of potential targets of cyber-attacks; or permitting the evasion of human control or oversight through means 26
of deception or obfuscation. Models meet this definition even if they are provided to end users with technical 27
safeguards that attempt to prevent users from taking advantage of the relevant unsafe capabilities.43 28
Fine-Tuning 29
An approach in which the parameters of an already trained model are adjusted by training on new data. Fine-30
tuning is often used to adapt a model to a particular task, or to mildly modify a model’s behavior. 31
Margin of Safety 32
The buffer that a developer may choose to leave between the level of risk associated with a model measured pre-33
deployment and the actual level of risk presented by its particular deployment to account for uncertainty in 34
capability evaluations and risk estimations. This margin could be, for instance, accounting for the additional time, 35
resources, and knowledge that malicious actors may have when assessing the amount of risk measured in a red-36
teaming exercise.  37
Misuse Risk 38
A risk that an AI model will be deliberately misused to cause harm. Pursuant to the NIST AI Risk Management 39
Framework (AI RMF),44 risk is defined as the composite measure of the probability that a harm occurs and the 40
magnitude (or degree) of the corresponding harm. 41
Model Flaws 42
Issues in a model that could lead to misuse risk, such as security vulnerabilities and other model safety issues, 43
including weaknesses in model safeguards.  44

<!-- page 28 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

23

Model Performance  1
A model’s capability and adaptability to a new task or unseen data, which may, but does not necessarily include, a 2
model’s accuracy.  3
Unauthorized Access  4
Obtaining without permission information that substantially aids an actor in recreating an AI model or its 5
capabilities that may introduce misuse risk, such as the code or weights that define the model, or bypassing 6
security measures designed to prevent access to the model itself such that an actor can utilize AI model 7
capabilities in an unauthorized manner. Depending on the stage in the AI lifecycle and how the model is deployed, 8
categories of unauthorized access may have differing degrees of relevancy. 9
Proxy Models 10
Deployed models that may have similar capabilities to the model and thus be most pertinent to estimating the 11
risks of misuse. 12
Threat Profile 13
A threat profile consists of: (a) the malicious task(s) that the threat actor might accomplish using the model, (b) the 14
threat actor or actors who might use the model to cause this type of harm, (c) the way(s) in which they could use 15
the model to accomplish this task, and (d) the mechanism(s) by which this could cause harm.  16

<!-- page 29 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

24

Appendix B. Example Methods to Mitigate Misuse Risk 1
The available mitigations against the misuse of foundation models continue to evolve and 2
expand. Current literature suggests that mitigations’ effectiveness can vary widely, and reliance 3
on them to prevent misuse should be based on empirical evidence of the mitigations’ efficacy, 4
particularly as some may incur tradeoffs in areas like cost, transparency, researcher access, and 5
user privacy. The following table provides a non-exhaustive survey of several categories that 6
organizations can consider: 7
 8
Table 1. Example Risk Mitigations. 9
Risk Mitigations Possible Implementation Methods
Improve the
model’s training.
• Filter training data to exclude examples that could result in capabilities that increase
the likelihood of misuse, such as biological sequence data, or known CSAM/NCII
images.45
• Apply refusal training and similar training techniques to enhance a model’s ability to
refuse harmful requests.46
• Train models with approaches that make it more difficult for subsequent fine-tuning
to remove safeguards.47
• Consider employing machine unlearning approaches, such as exact unlearning,
approximate unlearning, zero-shot learning (ZSL) and fast and efficient unlearning, to
reduce the model’s knowledge of harmful information.48
Detect and block
attempted
misuse.
• Add additional infrastructure around the base model to monitor for and detect
behavior which may constitute misuse—such as with algorithmic classifiers for
misuse. This infrastructure should be supported, as appropriate, by human review.49
• Once detected, block, modify, or otherwise limit unsafe queries and responses, and
place limitations on users and organizations engaging in misuse or attempting to
circumvent safeguards.
• For available weights, maintain a feedback mechanism to learn of misuse incidents
and work with model hosting platforms to address distributions that are intended to
increase misuse.
Reduce or limit
access to the
model’s
capabilities.
• Limit access to the model, or to versions or features of the model that display
particularly high-risk capabilities, to users with lower risk of misuse and contexts that
are easier to monitor.50
• Reduce access to the model reactively when misuse is detected to limit further
misuse, such as by rolling back a model to a previous version or discontinuing
availability of a model, if a model displays sufficiently extreme misuse risk while it is in
production.
• Consider limiting internal access to the models’ weights within an organization.
• Consider when it is appropriate to allow the model to be fine-tuned via API, which
also can reduce the availability of safeguards, such as by letting users train the model
on data related to dangerous tasks or reduce how often the model refuses dangerous
requests.51
• Iteratively deploy systems so as to observe real-world capabilities and monitor for
misuse from weaker systems.
• For models that pose sufficiently severe risk, consider restricting and monitoring
access even by individuals directly involved in its development and evaluation.
Internal protections can reduce the risk that an organization’s own employees or
contractors are able to misuse models; these protections can include logging

<!-- page 30 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

25

employee interactions with models, restricting model access to a subset of
employees, requiring multiple employees to access a model together, and ensuring
that all employee interactions with the model are accompanied by the model’s other
relevant safeguards.
Release the model
in stages.
• Consider deploying a model via an API to understand its impacts before making its
weights available, such as by making them available for download by the public.
• Consider the fact that once a model’s weights are made widely available, options to
roll back or prevent its further sharing and modification are severely limited.52
• Consider deploying a model with a limited audience and gradually expanding access
to the model to wider audiences (e.g. work with cybersecurity professionals to fix
bugs or carry out large scale testing before a model is widely available).53
Collaborate across
the supply chain
to implement real-
world protections.
• Collaborate with cybersecurity professionals to fix issues such as infrastructure
vulnerabilities.
• Collaborate with the scientific community to improve practices such as nucleic acid
synthesis screening, a biosecurity practice that aims to control access to dual-use
biological materials, rendering it more difficult to carry out a biological attack.54
• Collaborate with other actors to improve filtering and protect against AI-enabled
fraud.
Stop developing a
model if it
presents
significant misuse
risk.
• If other practically available safeguards are not sufficient to protect a model from
misuse–including considering the risk of unauthorized access or internal abuse–then
it may be appropriate to make significant changes to the development plan, including,
if necessary, delaying the development of the model.
 1

<!-- page 31 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

26

Appendix C. Key Characteristics of Measurement Tasks 1
This table provides a non-exhaustive overview of approaches to measure misuse risk to use in 2
accordance with the recommendations provided in Practice 4.1. This table is based on the 3
current state of the field, and organizations should recognize that these characteristics will 4
likely change as the science of risk measurement evolves. 5
Table 2. Measurement Task Characteristics. 6
Measurement Environment
Measurement tasks can evaluate model capabilities in various environments, some of which are outlined
below.
Environment type Description Examples
1. Question &
answer
The model is given static prompts (whether
text, images, or other modes), and its
response is scored.
- The model is run on MMLU,
GPQA, and other widely used,
public benchmarks.55
2. Question &
answer with
tools
The model is given static prompts, but it can
interact with a computational environment
containing relevant tools or workspaces to
draw conclusions and inform a response.
Note that the inclusion of tools may provide
a better indication of system performance
under realistic conditions.
- When answering mathematical
reasoning questions, the model
is provided with a scratchpad for
Chain-of-Thought reasoning and
the ability to write and run Python
code.
- When answering biological
questions, the model is provided
with relevant domain-specific
tools that a human would use in
their work, such as
bioinformatics tools.
3. Computer
environment
The model is given a task to complete and
access to versions of standard OS utilities
such as shells, interpreters, and a text
editor, to interact with computer systems or
other computers over a network. These
evaluations can be automatic while still
closely matching some realistic
deployments.
- A capture the flag challenge in
which the model runs arbitrary
code on a local machine to
attempt to compromise a remote
server.
- A machine learning challenge
that provides the model with a
training data set and the system
runs within a docker container to
submit a trained model that is
scored using a hidden test set.
4. Human
interaction
The model exchanges messages with
humans, which can be accompanied also
with interactions with computer
environments and tools.
- The model negotiates with a
human participant as part of a
controlled experiment, and the
participant grades model
performance on a set scale.
- A biosecurity expert asks a series
of questions to the model to
simulate an interaction with a
malicious actor. The expert
grades the model responses
using a provided rubric.

<!-- page 32 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

27

5. Physical
environment
The model interacts with physical systems.
Evaluations usually involve physical
experiments in which the model controls
physical actuators (or gives advice to
humans to take physical actions) based on
observations of the environment.
- The model advises a human on
how to carry out a procedure in a
biology lab. A human carries out
the instructions and the results
are assessed.
- The model controls a drone to
evade obstacles and reach a
target.
6. Simulated
environment
When conducting physical experiments is
expensive, it may be possible to collect
approximate results by simulating a
realistic environment and measuring model
capabilities in that simulation.
- The model advises a human on
carrying out lab protocols in a
virtual reality simulation of a
biology lab.
- The model interacts with a
computer environment in which
the role of human users is
simulated by another model.
Grading Procedure
Measurement tasks can evaluate model capabilities using various grading procedures, both qualitative
and quantitative, some of which are outlined below.
Grader Description Examples
1. Known
ground truth
Reponses to questions are graded by a
simple and unambiguous rule for
determining which responses are correct
(or how to award partial credit). Note that
this method only works for specific
questions (see non-exhaustive examples).
- Multiple-choice questions can
be graded by comparing an
answer to the ground truth.
- Numerical questions can be
graded by comparing numerical
values.
2. Interpreting
results
based on a
rubric
A subject matter expert reviews model
output to judge whether it is correct or
whether analogous responses would be
useful to a malicious actor in a realistic
misuse context. These reviews may also be
automated by an AI system equipped with a
task rubric, although automated grading
can introduce further error.
- The model is tasked with
producing detailed instructions
for carrying out a real-world task,
and an expert judges whether
those instructions are precise
and accurate enough to be
useful for a malicious actor.
- The model carries out multiple
steps of a simulated offensive
cyber operation, and an expert
reviews its behavior to assess
how well the model might
perform in a more realistic
setting.
3. Environment
al objective
The model is graded in an interactive
environment based on whether it has a
certain effect on the environment.
- In a software engineering
evaluation, the model can be
scored based on whether it
writes software that passes unit
tests and how many resources it
consumes while doing so.
- In a laboratory uplift experiment,
the model that is helping novices
troubleshoot a lab protocol can
be scored based on physical

<!-- page 33 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

28

measurements of whether those
protocols were successful.
Model Involvement in Measured Task
Measurement tasks can evaluate misuse risks that involve various levels of model autonomy, such as the
model automating an end-to-end task or the model providing a human marginal ‘uplift’ on an existing task,
some of which are outlined below.
Evaluated
system
Description Examples
1. Fully
autonomous
system
An AI system, which incorporates a
foundation model, solves an evaluation
task fully autonomously. Although most
misuse tasks involve an instruction and/or
other aid from a malicious actor to the AI
system they are using as a tool, for some
misuse scenarios there may still be
evaluated subtasks that are fully
automated.
- A capture the flag challenge in
which the model autonomously
identifies vulnerabilities and
develops an exploit.
- A question-answering task in
which the model uses tools and
web research to write
instructions for a complex task
that are graded by an expert.
2. Human + AI
system
activity
(“uplift
study”)
A human uses an AI system, which
incorporates a foundation model, as an
assistant to accomplish an evaluation task.
For many tasks there is no simple
decomposition of a task into subtasks that
are performed by an AI system and
subtasks performed by humans. In these
settings, evaluating the performance of a
human-AI team is the only way to obtain a
directly meaningful indicator of
performance. Such evaluations may
consider humans with limited expertise
being able to achieve previously
unobtainable outcomes by using an AI
system.
- A capture the flag challenge in
which a human uses an AI tool to
help them more quickly identify
vulnerabilities and develop an
exploit to extract a flag.
- A question-answering task in
which human novices use an AI
assistant to write instructions for
a complex task that are graded
by an expert.
- A laboratory uplift study in which
human participants use an AI
system as an assistant to
propose and troubleshoot
protocols to achieve a real-world
goal.
Conclusions Drawn from Measurement
Different evaluation tasks provide varying degrees of information for which conclusions about the model
can be drawn. For instance, some measurement methods, such as monitoring the impact of the model in
the wild, can inform organizations’ understanding of a model’s absolute performance, whereas other
assessments should be used only to assess performance relative to another model or a human baseline
Conclusion
Drawn
Description Example
1. Absolute
performance
on a task that
is
representativ
e of real-
world risk
Some measurements are sufficiently
representative of real-world misuse
scenarios. For these tasks, it may be
possible to draw a direct correspondence
between the measured level of
performance on the task and the model’s
potential real-world impact.
- The model is used to identify
vulnerabilities and create and
execute exploits for real-world
software. These results may
provide direct evidence of the
model’s usefulness in
automating an offensive cyber
task.
- Novices use the model to
troubleshoot lab protocols

<!-- page 34 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

29

similar to those needed to
develop a bioweapon. These
results may provide direct
evidence of the tool’s usefulness
in a malicious biological
workflow.
- The model’s ability to identify
vulnerabilities and create
exploits for real-world software
is related directly to a model’s
ability to enable that misuse risk
in the wild.
2. Performance
on a task
relative to
another
model or a
human
baseline
Some measurements may be less directly
comparable to a real-world misuse
scenario. Instead, they involve capabilities
that are similar enough to provide some
useful signal, particularly about the relative
performance of different models (or the
comparison between model and human
performance). Such measurements may
provide an indicator of whether the model
may significantly alter misuse potential
beyond existing baselines. Combined with
other evidence about the misuse potential
of a proxy model or human baseline, this
measurement can give evidence about the
misuse potential of the model.
- Comparing the performance of
two models on cyber capture the
flag challenges to get an
indicator of whether one of them
is likely to be significantly more
useful for vulnerability
exploitation than the other.

Relationship to Misuse Scenario
The relationship between the measurement task and the actual misuse task may vary, which can impact
how useful the measurement is for assessing real-world misuse risk and whether the measurement is
better suited to absolute or relative risk assessment.
Relationship to
misuse task
Description Examples
1. Close match
for misuse
task
In some cases, it is possible to safely
evaluate tasks from essentially the same
distribution that would be used by a
malicious actor, or to monitor real-world
misuse.
- An authorized attempt to
compromise a real IT system.
- Monitoring the impact of AI-
generated synthetic content in
the wild.
2. Safe proxy
for misuse
task
In some cases, it is possible to modify a
task in a way that reduces the risk of
carrying out the measurement without
changing the capabilities that would be
required to succeed at the dangerous
variant of the task.
- Measuring a model’s ability to
help a human synthesize a safe
biological agent with similar
properties to a dangerous
bioweapon.
3. Subtask of
misuse task
Sometimes it is easier or safer to evaluate
individual steps or tasks in a more complex
misuse task or chain of tasks, and weak
- Having novices use the model to
carry out particular steps of
dual-use biological protocols

<!-- page 35 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

30

 1
performance on an individual subtask can
provide a strong indication that a model will
not perform well at a more complex end-to-
end task.
that are particularly challenging
or inaccessible.
- Asking the model to identify and
fix a simple flaw in a piece of
malware.
4. Requires
similar
capabilities
to misuse
task
Tasks that experts consider to involve
similar skills to a misuse task can also be
used to measure misuse risk. The quality of
inference depends on the degree of
similarity. When tasks are only distantly
related, then the evidence can only be used
in settings where large error is acceptable
(such as establishing a conservative bound
on capabilities).
- Evaluating the model’s ability to
generate explicit videos of adults
to provide partial evidence of
their ability to do so for minors.
- Studying the benign usage of
models in real-world biological
laboratory settings.
5. Simpler than
misuse task
In many cases, experts may have some
confidence that one task is significantly
easier than another loosely related task,
even if they are uncertain about the exact
relationship. This can provide evidence that
an AI system does not pose a significant
misuse risk even if there are important
differences between evaluation and misuse
tasks.
- Evaluating the model’s general
scientific capabilities using a
question-answer dataset
designed to be much easier than
autonomously facilitating novel
scientific discoveries.
- Evaluating the model’s ability to
identify security-critical flaws in
short snippets of code designed
to be much easier than finding
vulnerabilities in realistic
software.

<!-- page 36 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

31

Appendix D. Application of NIST AI 800-1 to Chemical and Biological 1
Misuse Risk  2
This appendixxii outlines additional considerations relevant to identifying, measuring, and mitigating risks 3
associated with the misuse of foundation models for the development or use of dangerous biological or 4
chemical agents. This appendix’s goal is to complement the broader set of objectives and practices 5
outlined in the main body of the guidance by assisting developers, deployers, and other actors across 6
the AI supply chain in understanding domain-specific considerations that can assist in implementing 7
misuse risk management practices. The recommendations in this appendix are primarily relevant for 8
foundation model developers and deployers, as well as third-party evaluators that work with developers 9
and deployers to help assess chemical and biological misuse risks. Other actors’ roles are discussed in 10
Section 3 of the main document.  11
 12
The assessment of AI misuse risks, particularly for foundation models, is a rapidly evolving field requiring 13
expertise across multiple domains including cybersecurity, biosecurity, and national security. The 14
guidelines in this appendix represent initial considerations to assist organizations in approaching these 15
complex challenges. These documents are being released for public comment and further review. U.S. 16
Government (USG) entities, along with state, local, tribal, and territorial government actors and law 17
enforcement agencies, possess unique insights, expertise, and access to sensitive information regarding 18
threat actors, historical incidents, and emerging scenarios that are essential for comprehensive risk 19
assessment in the domain of chemical and biological misuse. This expertise can complement private 20
organizations’ technical understanding of foundation models’ capabilities, and future work may explore 21
how public and private expertise and risk assessments can work together.  22
  23
D.1 Identifying Chemical and Biological Misuse Risk  24
This section expands on Objective 1 (“Identify potential misuse risk”) for identifying chemical and 25
biological (CB) misuse risks from foundation models. The potentially high-consequence and cascading 26
effects of CB agents, particularly novel agents and/or toxins and transmissible biological agents, 27
necessitate careful identification of potential risk.56 As outlined in Practice 1.3, organizations should 28
assess both the likelihood of successful misuse and the impact of possible consequences. Risk 29
assessment in this domain represents an interplay between organizations and government entities, with 30
each bringing distinct and complementary capabilities and insights to the process. While organizations 31
such as developers and deployers can assess a foundation model’s technical capabilities, USG entities 32
can provide critical context about threats, actors, and scenarios that enable comprehensive risk 33
evaluation.  34
  35
CB risk assessment involves analyzing the intersection of two rapidly evolving fields: AI and 36
biotechnology. Risks may emerge not just from improvements in foundation models, but from how 37
these models interact with new biotechnology tools and techniques.  38
  39
In assessing CB misuse risks, organizations such as developers, deployers, and third-party evaluators can 40
focus on evaluating a foundation model’s technical capabilities and how these capabilities might affect 41

xii Note: While the concepts in this appendix align with the main text of 800-1, some section numbers and cross-
references may not match exactly between the documents.

<!-- page 37 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

32

existing barriers to misuse, while USG entities can provide organizations with appropriate threat profiles 1
for evaluation purposes. For emerging risks without extensive historical precedent, organizations can 2
work with USG entities to understand how capability changes could affect different threat scenarios and 3
identify potential defensive measures.  4
  5
D.1.1 Establishing Threat Profiles: Actors and Scenarios   6
When establishing and prioritizing CB misuse scenarios for assessing foundation model capabilities, 7
organizations typically benefit from working with subject matter experts (SMEs). SMEs can help analyze 8
how a model might enhance different actors’ abilities to accomplish measurable CB tasks that could 9
enable harm. Such an analysis might focus in particular on how a foundation model could reduce 10
capability barriers for less sophisticated actors. To aid this work, organizations can build on existing 11
frameworks for assessing life sciences dual-use research of concern57 to incorporate AI-specific 12
considerations,58 such as by documenting when and how specific measurable chemical and biological 13
misuse risks may arise (see Table D.4). Where they already exist, organizations may use established 14
frameworks for identifying AI-specific CB misuse risks to complement the guidance in this document.  15
  16
As outlined in Practice 1.2, when establishing CB misuse scenarios, organizations can identify 17
representative threat profiles to help categorize and prioritize the risk space, focusing on those most 18
relevant to a specific foundation model’s capabilities. While the distribution of such a list requires 19
careful consideration of potentially sensitive information, it helps ensure no major categories of risk are 20
overlooked and allows for more transparent justification of which scenarios to prioritize for deeper 21
analysis.  22
  23
The following subsections outline relevant factors and example methods that organizations can consider 24
when analyzing potential misuse scenarios and threat profiles, including actor categories, scenario 25
types, and key barriers that foundation models might aid an actor in overcoming. Detailed threat 26
profiles are primarily necessary when a foundation model may advance the frontier of CB capabilities 27
available to malicious actors. In other cases, and for other capabilities, organizations can typically rely on 28
simpler risk assessment approaches, such as comparisons to proxy models as outlined in Practice 1.1, or 29
existing frameworks.  30
  31
Threat Actor Categories. To enable better scoped and more effective risk assessment and mitigation 32
strategies, organizations can distinguish between state actors (who often have access to multiple expert 33
scientists, extensive resources, and specialized facilities, and may pursue strategic national objectives) 34
and non-state actors (who typically face various resource and expertise constraints and may have 35
different motivations). To facilitate more consistent assessment across organizations, the following 36
illustrative non-state actor profiles could be considered:  37
• Organized violent non-state group with multiple members, some funding, and potential access 38
to relevant facilities.  39
• Individual with advanced scientific expertise (e.g., PhD or equivalent experience in a relevant 40
biological subfield).  41
• Lone actor or small group with malicious intent but limited expertise and resources.  42
  43
For each actor category, capabilities and sophistication can be assessed across multiple dimensions, 44
such as:  45

<!-- page 38 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

33

• Scientific expertise and laboratory experience (including quality and quantity of research 1
experience, tacit knowledge, and technical support networks).  2
• Available time and operational constraints (including both self-imposed and external timeline 3
pressures).  4
• Ability to acquire necessary materials (including access to facilities, suppliers, and financial 5
resources).  6
• Ability to access and use foundation models (including elicitation capabilities such as tooling 7
development, potential for model weight exfiltration, fine-tuning on private datasets, and 8
circumvention of safeguards).  9
  10
Organizations may also consider assessing both deliberate misuse by malicious actors and unintentional 11
harm from researchers or organizations lacking sufficient safety expertise or oversight.59  12
  13
Threat Scenarios. To better understand the range and severity of potential harms, organizations can 14
consider threat scenarios across different agent types and intended outcomes. High-level examples 15
include, but are not limited to:  16
• Acquisition and/or release of a known transmissible biological agent that could seed an 17
epidemic or pandemic.  18
• Acquisition and/or release of a known chemical or non-transmissible biological agent over a 19
high-density or large population area or in a transportation hub, urban event, or other 20
congregate setting.  21
• Design, acquisition, and/or release of an enhanced or novel chemical or biological agent.  22
  23
Organizations can use the above high-level threat scenarios as a starting point for more specific and 24
comprehensive CB threat scenarios. These could be similar to the list of example biological and chemical 25
threats in the Homeland Security Planning Scenarios.60  26
  27
Barriers and Model Capabilities. To identify specific ways that foundation models might increase risk, 28
organizations can assess how foundation models might help actors overcome existing barriers, such as:  29
• Technical Barriers: Technical barriers relate to scientific challenges in the end-to-end synthesis, 30
acquisition, and delivery of chemical or biological agents. Key examples include tacit knowledge 31
requirements for agent-specific synthesis and experimental manipulation, genome design and 32
assembly challenges, interdisciplinary expertise gaps, and laboratory troubleshooting 33
capabilities. Foundation models may reduce these barriers through detailed guidance and 34
assistance, including in multiple modalities.  35
• Operational Barriers: Operational barriers involve logistical challenges such as facility 36
requirements, equipment and material limitations, financial and time constraints, headcount 37
requirements, and industry screening of customers or orders. While models cannot directly 38
address physical infrastructure needs, they may help actors identify minimum necessary 39
requirements, aid in execution of tasks within a laboratory, suggest alternative approaches to 40
achieving the same capabilities with different methods or materials when preferred options are 41
unavailable, or explore ways to circumvent existing biosafety61 and biosecurity62 controls.  42
• Motivational Barriers: Motivational barriers include the initial ideation of using CB agents as 43
weapons for specific goals, perceived difficulty of developing and using CB agents as weapons, 44
as well as psychological and normative barriers such as fear of attribution or international 45
norms. While some actors may be more willing to overcome these barriers based on their 46

<!-- page 39 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

34

beliefs or objectives, model assistance could make complex processes appear more manageable 1
and reduce the need for collaborators. Organizations may consider how their models’ responses 2
to CB-related queries might affect these barriers.  3
  4
D.1.2 Risk Assessment  5
After identifying key threat profiles, organizations can identify which scenarios warrant detailed 6
assessment. The process of assessing CB misuse risks requires close coordination between organizations 7
and USG entities. Organizations’ technical understanding of foundation models complements USG 8
expertise regarding threats and scenarios. To ensure efficient use of assessment resources, 9
organizations may first identify a set of representative scenarios spanning different scales of potential 10
harm (e.g., varying levels of health, economic, or national security impacts), then evaluate these 11
scenarios using the following three factors:  12
• Severity of Potential Harm: The magnitude and scope of potential harm if an actor successfully 13
executes the threat scenario. This may be particularly important for scenarios involving 14
transmissible biological agents that could cause cascading effects beyond initial release or 15
agents for which there are no reliable medical countermeasures. Impacts can span across 16
multiple categories, including but not limited to: human health effects (i.e., illnesses and 17
deaths); impacts to animal, plant, and environmental health; harm to U.S. national security or 18
economic security; and broader societal disruption. Organizations can consider how different 19
combinations of reduced barriers might affect potential harm.  20
• Counterfactual Effect: The marginal increase in risk that foundation models might create 21
beyond baseline capabilities, which can vary across actors. Some threat actors may already have 22
a high likelihood of success through certain pathways (such as synthesis of known pathogens in 23
professional laboratory settings or acquisition of industrial chemicals through legitimate 24
suppliers), making the additional impact of access to a foundation model’s capabilities less 25
significant for these scenarios.  26
• Likelihood of model enabling actors to overcome barriers: The likelihood that foundation 27
models will develop capabilities that enable actors to overcome specific barriers within the 28
assessment timeframe. This varies significantly by barrier type – for instance, models may more 29
readily help overcome technical barriers like laboratory protocol development than operational 30
barriers like acquiring specialized equipment. Organizations can incorporate both technical 31
feasibility and anticipated model development trajectories when assessing this likelihood.  32
  33
For scenarios identified as high priority through the above analysis, organizations can assess how model 34
capabilities might affect technical success rates and reduce existing barriers across different types of 35
actors. When working with relevant USG entities, additional context may be available to inform these 36
assessments, including:  37
• Threat actor profiles and characteristics.   38
• Technical and operational factors that influence success rates.  39
• How capabilities might affect different categories of actors.  40
  41
This collaborative approach enables organizations to contribute their deep understanding of model 42
capabilities while drawing on USG expertise regarding threat scenarios, actor profiles, and assessments 43
of potential threat actors and likelihood of misuse attempts. Together, this allows for more 44
comprehensive evaluation of how a foundation model’s capabilities might affect risk within specific 45
scenarios.  46

<!-- page 40 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

35

  1
These assessments can consider:  2
• Baseline risk.   3
• Marginal risk from model access (how a model might expand actor pools, improve success rates, 4
or increase potential impact through enhanced capabilities or novel techniques).  5
• The impact of different combinations of overcome barriers on risk (e.g., overcoming technical 6
but not operational barriers may limit potential impact).  7
• Existing defensive measures and controls (like biosurveillance systems and nucleic acid synthesis 8
screening) that are publicly documented and how foundation models might enhance such 9
measures and controls.63   10
  11
It is useful for organizations to draw on historical CB incidents and SME expertise to inform these 12
assessments. The group of SMEs is often most valuable when it has demonstrated expertise in both the 13
relevant scientific and technical domains (virology, synthetic biology, machine learning, etc.) as well 14
security (biosecurity, national security, etc.). This can include using structured expert elicitation 15
methods, such as the Delphi method, and noting areas of expert agreement and disagreement. While 16
precise quantification may be challenging, organizations can document:  17
• Key assumptions and evidence about foundation model capabilities.  18
• How capabilities vary across deployment contexts.   19
• Relative weighting of different risk factors and treatment of uncertainties.  20
  21
These assessments can be updated by organizations with access to relevant SME expertise as new 22
evidence emerges about model capabilities through observation of legitimate use (e.g., model 23
assistance for beneficial research) and malicious misuse attempts.  24
  25
Information Sharing Considerations. After conducting CB risk assessments, organizations may carefully 26
weigh transparency benefits against publicizing potentially sensitive information, making sharing 27
decisions on a case-by-case basis. Organizations may consult with USG entities regarding potentially 28
sensitive findings. Examples of information that may be useful to share publicly include:  29
• The general framework used for creating threat scenarios or profiles.  30
• High-level categorization of threat actors.   31
• The dimensions considered in capability assessment (scientific expertise, material acquisition, 32
model access).  33
• The key factors used in scenario prioritization (counterfactual effect, likelihood, severity)  34
• General approach to risk quantification methodology.  35
• Descriptions of how expert panels are sourced and structured.  36
  37
Some examples of information that may require careful consideration before sharing and may be more 38
appropriate to share with a limited group include:  39
• Detailed threat scenarios or profiles.  40
• Quantitative or qualitative risk estimates for specific scenarios.  41
• Novel risk pathways identified during assessment.  42
• Detailed information about routes to CB acquisition.  43
• Detailed information about routes to harm, including specific steps in the CB attack chain (e.g., 44
synthesis, weaponization, delivery).  45
• Information about specific pathogens.  46

<!-- page 41 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

36

  1
D.1.3 Key Opportunities and Challenges for Risk Assessment  2
  3
Opportunities:  4
• Laboratory processes’ structured nature and clear technical requirements enable systematic 5
analysis of the impact of assistance from foundation models 6
• Existing life sciences dual-use research frameworks provide valuable precedent for evaluating 7
dangerous capabilities of foundation models 8
• Risk assessment methodologies can effectively break down complex scenarios into analyzable 9
components  10
  11
Challenges:  12
• The complex interplay between actor sophistication levels and their ability to overcome various 13
barriers makes mapping model performance on a task to actual risk difficult  14
• Limited historical data on CB attacks complicates baseline risk estimation  15
• Balancing scientific transparency with security considerations may require careful consideration 16
given the benefits of transparency and the potential risks of disclosing novel information 17
regarding CB risk pathways  18
  19
D.2 Evaluating Chemical and Biological Capabilities Relevant to Misuse 20
Risk  21
Building directly on Section 5, Objective 4 (“Measure misuse risk associated with model deployments”) 22
and the measurement characteristics in Appendix C, this section provides detailed guidelines for 23
evaluating CB misuse risks. Organizations can refer to Appendix C’s framework while implementing the 24
CB-specific guidelines provided here.  25
  26
D.2.1 CB Evaluation Types and Characteristics  27
When designing foundation model evaluations for CB misuse risk, organizations can account for the 28
rapid pace of advancement in both AI and biotechnology – particularly how emerging tools and 29
techniques might create new risk pathways. The following evaluation types provide a framework that 30
can be adapted as capabilities in both domains continue to advance.  31
  32
Building on Appendix C, organizations can employ multiple complementary evaluation approaches to 33
build a more comprehensive understanding of potential misuse tasks while maintaining documentation 34
of methodologies and results. This section focuses on evaluating foundation models on CB assistant 35
tasks, especially in laboratory contexts. Other capabilities, such as those of specialized chemical and 36
biological AI models64 like protein design models, are also important potential sources of risk, but 37
evaluating the capabilities of such models typically involve other measurement approaches.  38
  39
Common evaluation types for CB misuse risk include the following:  40
• Automated Benchmarks: These are standardized question-answer sets that enable rapid, large-41
scale testing of model capabilities. For broad coverage of relevant CB misuse risks and 42
measurable tasks, automated benchmarks typically cover a broad range of CB topics with dual-43
use applications – usually comprising hundreds if not thousands of questions. Questions can be 44

<!-- page 42 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

37

multiple-choice or open-ended, with open-ended questions better resembling real-world 1
human-AI interactions.  2
• Assistant Task Evaluations: These evaluate a model’s ability to provide actionable guidance 3
when asked to accomplish specific tasks. The tasks can range from short-form focused queries 4
(e.g., “How would you modify this DNA plasmid sequence in X way?”) to long-form complex 5
multi-step processes (e.g., “Provide a complete protocol for the reverse genetics synthesis of 6
virus Y”). Task-based evaluations are intended to approximate actual human-AI interactions 7
better than automated benchmarks.  8
• Expert Model Assessment: This evaluation approach involves qualitative exploration of model 9
capabilities by SMEs (e.g., virologists, molecular biologists, biodefense experts) to help identify 10
potential areas of concern. Expert assessment typically takes two forms, which can be 11
combined: (i) SMEs evaluating model responses to assistant tasks for technical accuracy and 12
real-world feasibility, and (ii) SMEs engaging in exploratory dialogue with models to simulate 13
how malicious actors might attempt to elicit harmful information. Organizations can consider 14
using multiple expert teams tailored to each representative CB pathway being assessed.  15
• Uplift Studies: These evaluations assess how foundation models enhance human capabilities by 16
comparing the performance of humans with and without model assistance. While assistant task 17
evaluations measure model outputs directly, uplift studies measure success at specific 18
overarching tasks by measuring how effectively humans can use models to accomplish these 19
tasks. They focus on the combined human-AI results rather than the model results alone. While 20
expert model assessment can help identify potential risks, uplift studies generally provide more 21
reliable evidence about real-world capabilities since they directly measure what humans can 22
accomplish with model assistance. They include three main types: task operational uplift studies 23
(focusing on computational or web-based tasks), end-to-end operational uplift studies 24
(assessing performance across the entire ideation-to-release spectrum without physical 25
implementation), and full laboratory uplift studies (involving wet lab work).  End-to-end 26
operational studies, including several recent studies,6566 evaluate how dual-use foundation 27
models’ impact performance across different stages, while laboratory studies provide the most 28
comprehensive but resource-intensive assessment. Laboratory studies should be carefully 29
designed to understand safety risks while adhering to all applicable oversight frameworks, 30
policies, treaties, and regulations.  31
  32
Relationship to Misuse Tasks: When selecting evaluation approaches, organizations can consider how 33
closely they correspond to dual-use scenarios that could lead to realistic CB misuse scenarios. The 34
relationship between evaluation tasks and misuse tasks in the CB domain typically falls into one of five 35
measurement categories, as outlined in Appendix C: close match tasks, safe proxy tasks, critical 36
subtasks, tasks requiring similar capabilities, or tasks simpler than misuse tasks. In applying this 37
framework to CB evaluations:  38
• Close-match tasks and safe proxy tasks are the most direct measurement but are often difficult 39
to measure given safety and security considerations as well as laboratory requirements. Safe 40
proxy tasks, such as synthesizing benign viruses with similar technical characteristics to 41
dangerous ones, can provide comparable insights while reducing risk. Organizations should 42
ensure any such evaluations comply with all applicable regulations and oversight requirements.  43
• Critical subtasks, and tasks requiring similar capabilities, are particularly relevant in CB 44
evaluations as a second-best alternative to close-match and safe proxy tasks.  45

<!-- page 43 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

38

• Tasks strictly simpler than misuse tasks often have limited utility in certain risk scenarios as 1
state-of-the-art foundation models often match the performance of human experts on these 2
tasks.676869 There are exceptions to this, especially with respect to CB agent design and in silico 3
testing.  4
  5
Close-match measurement through laboratory work typically provides the most reliable evidence of 6
model capabilities. However, laboratory studies present significant challenges - including cost, the need 7
for specialized facilities and expertise, and safety and security considerations. Moreover, for tasks 8
relating to synthesis of dangerous CB agents, organizations typically find it valuable to pursue safe proxy 9
tasks rather than close-match tasks. When direct laboratory evaluation is not feasible, organizations can 10
employ two key alternative measurement approaches:  11
1. Comparable Task Assessment (corresponding to safe proxy tasks, critical subtasks, and tasks 12
requiring similar capabilities in Appendix C): CB evaluations usually involve safe comparable 13
tasks or subtasks that maintain technical similarity while reducing evaluation-related risk. 14
Organizations can validate the relationship between comparable or similar task and actual task 15
performance through scientific and national security expert assessments,70 document 16
assumptions about how comparable task performance relates to real-world capabilities, and 17
consider multiple comparable tasks to triangulate capability assessment. For example, when 18
assessing capabilities related to viral agent synthesis, organizations might evaluate performance 19
on synthesizing harmless viral proxies that maintain technical similarity while reducing biosafety 20
and biosecurity risks of performing viral agent synthesis in a laboratory setting.  21
2. Proxy Model Comparison (corresponding to the relative risk measurement approach in 22
Appendix C): Organizations can compare their model’s performance against existing widely used 23
models whose risks and capabilities are better understood. For example, if model A has been 24
tested in laboratory uplift studies and found to provide sufficient uplift for viral synthesis, a 25
developer might conclude that model B presents a manageable risk by finding that it has 26
significantly lower performance than model A on question-answering tasks related to laboratory 27
troubleshooting. This allows organizations to leverage existing knowledge about the relationship 28
between different types of tasks while minimizing safety and security risks in their own testing. 29
This approach is especially valuable for organizations with limited resources as it necessitates 30
less extensive testing infrastructure.  31
  32
D.2.2 Considerations for CB Evaluation Methodology  33
CB evaluation methodologies can incorporate several key elements across evaluation types to help 34
ensure comprehensive and reliable assessment. To promote safety across the AI supply chain, these can 35
be shared as part of transparency reports or system cards. Additional considerations for the following 36
categories include:  37
  38
Design of Automated Benchmarks and Assistant Task Evaluations:   39
• Considerations:  40
o For multiple-choice questions, include carefully crafted options with plausible 41
distractors to prevent models from using choice elimination strategies,71 and validating 42
format effectiveness through small-scale comparisons with open-ended versions. Open-43
ended questions better approximate real-world interactions, focusing on information 44
integration, error identification, and novel knowledge application rather than factual 45
recall alone.   46

<!-- page 44 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

39

o Task-based evaluations typically use clear rubrics assessing technical accuracy, 1
completeness, and real-world feasibility, often employing tiered scoring to account for 2
partially correct responses. Where possible, assistant task evaluations can be validated 3
against uplift studies to confirm that expert assessments correlate with real-world 4
success rates.  5
• Transparency: Organizations can specify how they developed the questions, how they ensured 6
quality control, the extent to which the questions or tasks reflect real-world workflows, 7
comparisons of results against previous evaluation efforts when available, and other relevant 8
factors.  9
  10
Design of Expert Model Assessment:   11
• Considerations:   12
o In expert model assessment, SMEs with relevant CB expertise (such as in virology, 13
synthetic biology, and biosecurity) can assess the model’s responses for accuracy and 14
utility, providing a subjective assessment of how useful the model’s response would be 15
for an actor attempting to misuse the agent.   16
o To maintain consistency and reduce subjective variation, organizations can establish 17
structured evaluation formats and maintain consistent assessment criteria across 18
evaluations while documenting methodology to enable comparison across models. 19
Emerging automated expert assessment systems may complement human evaluation, 20
though these approaches are still being developed for domain-specific assessment.  21
• Transparency: Organizations can specify the backgrounds of the experts, the rubric used for 22
assessment of the utility and accuracy of model responses, and other relevant factors.  23
  24
Design of Uplift Studies:   25
• Considerations:   26
o Uplift studies generally require sample sizes sufficient to rule out concerning effect sizes 27
and estimate improvements with clear error bounds. Studies can assess multiple metrics 28
relative to control groups, as task completion alone may miss important changes in 29
capability. Key metrics could include changes in protocol success rates, changes in 30
protocol completion speed, and changes in participant confidence and motivation 31
levels.   32
o Time frames reflect evaluation goals – if comparing to expert performance, allow 33
sufficient time for reasonable task completion; if comparing to malicious use scenarios, 34
match expected threat actor time constraints. If time must be reduced (for example, 35
condensing what would normally be a weeks-long project into hours), either decrease 36
task scope or increase available time proportionally.   37
o Participant expertise levels are meant to match threat actor profiles, with appropriate 38
expert control groups for capability comparisons. Studies can provide time to allow 39
participants to become familiar with prompt engineering and the model being studied, 40
use initial skill assessment through preliminary tests rather than self-reporting (e.g. first-41
day skill calibration), and prevent information sharing between groups. Analysis may 42
particularly focus on high-performing outliers, as these may represent significant risks 43
even when mean improvements appear modest.  44
o Organizations can consider different study designs to assess various aspects of capability 45
enhancement. This includes: (i) open-ended studies where participants must achieve an 46

<!-- page 45 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

40

end goal without being given a protocol, and (ii) protocol-based studies where 1
participants must identify and troubleshoot intentional errors or obstacles. Studies can 2
also evaluate different team configurations, from individual actors to small groups (e.g., 3
teams of 2-3 participants), as capabilities may vary significantly with team size and 4
composition.  5
o Laboratory uplift studies should be run for sufficient duration to accommodate multiple 6
attempts per task, as participants typically show significant improvement after initial 7
failures. These studies can incorporate both quantitative metrics and qualitative 8
observations of participant behavior and problem-solving approaches, with particular 9
attention to how participants interact with laboratory equipment and troubleshoot 10
experimental issues.  11
• Transparency: Organizations can specify sample size calculations and power analyses, time 12
allocation decisions, participant selection criteria, measures taken to prevent information 13
sharing between groups, and other relevant factors.  14
  15
Human Expert Baselines:   16
• Considerations:   17
o Establishing robust human expert baselines is crucial for contextualizing model 18
performance and assessing whether models are approaching or enabling non-expert 19
users to approach expert-level performance.   20
o Organizations can ensure high-quality expert participation by providing appropriate 21
incentives and access to all relevant tools and web-based resources for a level of 22
performance during evaluations that is reflective of human expert capabilities. Larger 23
expert group baselines can provide more reliable results.   24
o Expert grading should generally be blinded and assess multiple dimensions in addition 25
to accuracy, such as completeness, time-to-completion, innovation, and detection 26
avoidance. When assessing the ability of a foundation model to uplift the capabilities of 27
human novices, organizations may consider establishing a novice baseline and a direct 28
novice-using-foundation-model comparison.  29
• Transparency: Organizations can specify the backgrounds of the experts, how much time they 30
were given per question or task, what prompting guidance they were given when they 31
conducted such studies, and other relevant factors.  32
  33
Tool Integration and Multimodality:   34
• Considerations:   35
o Organizations can incorporate multiple modalities where relevant to CB tasks. For 36
example, image analysis capabilities may be useful for laboratory troubleshooting, 37
allowing models to interpret experimental results and identify equipment setup issues. 38
While currently underexplored, voice interaction capabilities may also become relevant 39
for hands-free model assistance during laboratory procedures.   40
o Foundation models can be tested with tools human experts typically use, including 41
literature search capabilities, bioinformatics software, and laboratory equipment 42
interfaces. For example, joint U.S. and U.K. AI Safety Institute pilot studies 43
demonstrated improved performance on DNA and protein sequence tasks when models 44
had access to Python sandboxes and bioinformatics packages.7273   45

<!-- page 46 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

41

o Organizations can consider how different augmentations may enhance model 1
capabilities, including:  2
▪ Retrieval-augmented generation systems that enable access to domain-specific 3
knowledge and reference materials  4
▪ Additional inference time and compute resources that enable longer reasoning 5
chains or additional attempts to respond to a request  6
▪ Tool use and API access that allow models to interact with external systems  7
o Examples of specific tools or scaffolds which may be relevant include, but are not 8
limited, to: literature search and retrieval-augmented-generation capabilities, 9
bioinformatics software via APIs or graphical interfaces, sandboxed versions of 10
commercial services like DNA synthesis providers, specialized biological or chemical AI 11
models for safe proxy tasks, and laboratory equipment interfaces where appropriate.   12
o Once a system is deployed, users may discover additional ways to improve its 13
performance or may use tools not contemplated during pre-deployment evaluations. 14
This gap is best considered when interpreting evaluation results, and organizations may 15
consider making forecasts about how performance may improve over time as available 16
tools and agent scaffolds improve.74  17
• Transparency: Organizations can specify which tools or multimodal interfaces were made 18
available to models and any limitations or constraints on tool or interface usage.  19
  20
Real-world grounding:   21
• Considerations:  22
o Organizations should ground their evaluations in empirical evidence when possible. For 23
example, if conducting yearly laboratory uplift studies, organizations might design 24
automated benchmarks that specifically test capabilities found to be critical in those 25
studies. Similar approaches can be applied to web-based tasks like sequence ordering.  26
o Organizations can consider clearly articulating why their chosen evaluation methods are 27
relevant to assessing real-world misuse risk. This could include explaining how each 28
evaluation relates to real-world CB tasks, and specifying which of the five measurement 29
categories it falls into and why their results are informative about misuse risk. They may 30
also justify why the level evaluation difficulty is appropriate (i.e., neither too easy nor 31
unrealistically hard).   32
o Organizations can include human participants where relevant, especially for longer, 33
complex tasks where human-AI interaction could significantly impact performance.75   34
• Transparency: Organizations can specify how evaluation tasks were derived from real-world 35
scenarios, what assumptions were made about task difficulty and complexity, and how human-36
AI interaction was incorporated into evaluation design.  37
  38
Interpreting multiple evaluation results:   39
• Considerations:  40
o Different evaluation approaches – even different configurations of the same evaluation 41
– can yield varying results about a model’s capabilities. For instance, a model might 42
perform differently when using different tool configurations, testing the same task using 43
different evaluation approaches, testing the same evaluation using different grading 44
methods, or otherwise evaluating under different conditions. This variation makes 45
interpretation of evaluation results challenging.   46

<!-- page 47 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

42

o Given the potential magnitude of real-world harms in CB, organizations can attempt to 1
measure tasks using diverse evaluation approaches, grading methods, and model 2
configurations during their internal pre-deployment testing and carefully document 3
these differences, erring on the side of caution when results conflict. Organizations can 4
take steps to minimize false negatives in capability evaluations – that is, to avoid 5
incorrectly concluding that a model lacks concerning capabilities.  6
• Transparency: Organizations can share evaluation results, including any apparent conflicts 7
between different evaluation approaches and remaining uncertainties. Organizations can also 8
share the number of runs conducted and inference parameters (temperature, top-p) used.  9
  10
Careful consideration of potentially sensitive information and other security-relevant issues: 11
Potentially sensitive information warrants particular attention when implementing and sharing the 12
results of evaluations meant to assess CB misuse risks. Organizations can carefully weigh the scientific 13
value of each measurement against the risk of revealing sensitive security-relevant information. This 14
includes considering both direct technical details and how multiple pieces of information might be 15
combined to cause harm. The ratio of beneficial to potentially harmful applications for any tested 16
capability is important to consider when disclosing information publicly. Moreover, there are legal and 17
regulatory frameworks, including export controls (including ITAR XIV76) and dual-use research of concern 18
requirements (including but not necessarily limited to the USG Policy for Oversight of Dual Use Research 19
of Concern (DURC) and Pathogens with Enhanced Pandemic Potential (PEPP)77), which may affect the 20
what, where, and how of communicating about CB evaluations. Given security considerations, some 21
information may be more appropriate to share with a limited group of organizations as well as 22
government and non-government third-party evaluators.  23
  24
D.2.3 Key Opportunities and Challenges for Measuring CB Risk  25
Current capabilities and measurement practices present several important opportunities and challenges 26
for assessing CB misuse risk:  27
  28
Opportunities:  29
• CB tasks typically enhance existing capabilities, enabling clear baseline comparisons with current 30
resources (e.g., internet use, bioinformatics tooling) and expert performance  31
• Increasing standardization of evaluation frameworks enables systematic risk assessment 32
through shared benchmarks and validated methodologies  33
• Multiple evaluation types allow effective triangulation of model capabilities and risks  34
  35
Challenges:  36
• Novel capabilities, especially in biodesign, are difficult to assess without existing baselines or 37
safe laboratory testing options  38
• Comprehensive risk assessment requires resource-intensive evaluation across the entire 39
ideation-to-release pathway  40
• Balancing scientific transparency with security considerations may require careful consideration  41
  42
D.3 Managing and Mitigating Chemical and Biological Misuse Risk  43
Building on the risk identification framework from D.1 and measurement approaches from D.2, this 44
section expands on Objective 2 (“Plan for managing misuse risk”), Objective 5 (“Mitigate misuse risk 45

<!-- page 48 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

43

before deployment”), and Appendix B (“Example Safeguards Against the Misuse of Foundation Models”) 1
to apply specifically to CB misuse risks. Organizations can use their measurement results to select and 2
calibrate appropriate safeguards for their context.  3
  4
D.3.1 Considering Dual-Use Dynamics in Risk Management  5
CB capabilities in foundation models present complex dual-use dynamics that can be broadly 6
categorized into three profiles:   7
• Predominantly Harmful capabilities with very limited legitimate applications 8
• High-Impact Dual-Use capabilities with significant legitimate applications but serious potential 9
for harm, especially regarding transmissible CB agents  10
• Mixed Dual-Use capabilities with many legitimate applications and some potential for misuse  11
  12
Based on specific risk assessments conducted as per Appendix D.1, organizations typically combine 13
multiple safeguards from Appendix B to achieve risk levels acceptable to the organization. 14
Understanding the relevant threat actors helps organizations implement proportionate security 15
measures. Many CB misuse risks can be managed through basic API restrictions and user verification 16
systems that keep out unsophisticated actors – for example, organizations may not need the highest 17
levels of information security for protecting model weights unless their threat assessment identifies risks 18
from sophisticated high-resource actors. These safeguards exist on a continuum rather than as binary 19
measures, with different implementations requiring varying levels of expertise and resources to 20
circumvent. Organizations can make evidence-based predictions about safeguard effectiveness against 21
different threat actor profiles and document how these predictions inform their risk management 22
decisions. Four safeguard approaches from Appendix B warrant particular attention in the CB domain:  23
1. Improve the model’s training: Filtering pre-training data to exclude certain types of CB-24
related content, such as viral and toxin data, and implementing refusal training for 25
harmful CB-related tasks may help reduce some risks while preserving beneficial 26
capabilities. However, this approach has multiple limitations: models’ performance at 27
relevant tasks may generalize across biological domains even if not trained explicitly on 28
certain CB agents, fine-tuning on excluded data can occur if model weights are 29
exfiltrated by a malicious actor, and researchers who wish to use model capabilities for 30
legitimate beneficial tasks may be impeded.  31
2. Detect and block attempted misuse: This is particularly important for "Predominantly 32
Harmful capabilities" with minimal legitimate uses, such as queries relating to the 33
circumvention of synthesis screening or dissemination of a CB agent. Relatedly, 34
robustness to jailbreaking attempts is important, which can be tested through red-35
teaming simulating sophisticated jailbreaking attempts.   36
3. Limit access to the model’s capabilities: Organizations can implement tiered systems 37
where different user categories have access to different capability levels, with each tier 38
combining appropriate access controls with other safeguards. For example:  39
▪ Mixed Dual-Use capabilities may merit basic identity verification and 40
monitoring  41
▪ High-Impact Dual-Use capabilities may also merit institutional affiliation 42
verification plus enhanced monitoring and detection systems  43
▪ Predominantly Harmful capabilities may have highly restricted access with 44
robust security measures, continuous monitoring, and comprehensive 45
safeguards against misuse 46

<!-- page 49 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

44

4. Collaborate across the supply chain to implement real-world protections: 1
Organizations may find it valuable to work with multiple types of suppliers and partners 2
to strengthen security measures. For example, they could work with DNA synthesis 3
providers to strengthen screening programs against AI-enabled circumvention attempts, 4
coordinate with biological resource centers that maintain and distribute pathogen 5
strains and pathogen-relevant cell lines to enhance verification of researcher credentials 6
and intended use, partner with cloud laboratories to monitor for suspicious patterns in 7
automated experiments, and collaborate with contract research organizations to 8
identify concerning requests for specialized research services. This could include 9
integrating AI model outputs with DNA synthesis screening through approaches like 10
cryptographically signed certificates that capture metadata about design provenance 11
and user intent.78    12
  13
If an organization has found its foundation model to potentially enable meaningful risk, it is useful to 14
document how implementing safeguards like those above will decrease risk prior to deploying the 15
model. This can follow a similar structure as the Estimation of Marginal Risk process in D.1. In general, 16
for capabilities that warrant higher security, organizations could consider implementing robust 17
information security measures.79   18
  19
D.3.2 Refining Risk Management Based on Real-World Evidence   20
The CB domain is dynamic and dual-use, with continuous advances in both legitimate research and 21
potential misuse pathways from both increases in foundation model capabilities as well as advances in 22
biotechnology. Organizations may gain significant insights about misuse risks after model deployment 23
based on real-world usage patterns and research by third parties. This information can help refine threat 24
assessments and mitigation strategies for both deployed and future models.  25
  26
The table in D.4 categorizes common CB-relevant measurable tasks and their use profiles to help inform 27
appropriate mitigation strategies. While this table presents capabilities as relatively standalone tasks, an 28
alternative and potentially more useful approach is to map specific capabilities along key risk pathways 29
of threat profiles.80 For example, measurable tasks could be analyzed according to their role in different 30
stages of a potential misuse pathway or mapped to specific technical processes like the laboratory steps 31
involved in viral reverse genetics. This pathway-based analysis can provide additional insight into where 32
and how different mitigation measures might be most effectively applied.  33
  34
D.3.3 Key Opportunities and Challenges for Managing CB Risk  35
Opportunities:  36
• Structured scientific research frameworks enable clear implementation of access controls and 37
monitoring systems  38
• Safeguards can be targeted to limit malicious access while enabling legitimate uses  39
  40
Challenges:  41
• The dual-use nature of scientific knowledge complicates designing safeguards that do not overly 42
restrict beneficial applications  43
• Severity of potential CB risks can require highly effective mitigations from initial deployment  44
  45
  46

<!-- page 50 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

45

Table D.4 Example Categorization of Potential CB Capabilities and 1
Associated Tasks  2
Task Category   Use Profile  Potential Benefits  Potential Risks  Potential Measurable Tasks/Subtasks
Scientific
Knowledge
Integration
Mixed Dual-
Use
Can enhance
research efficiency
and accelerate
scientific discovery
by making complex
information more
accessible and
actionable
Can enable
malicious actors to
efficiently plan
dangerous
experiments and
facilitate integration
of sensitive CB
information
• Hypothesis generation
• Experiment planning
• Literature review
• Integration of information from
multiple sources to form cohesive
insights
• New protocol development or
detail-filling via extrapolation from
other CB agents
Laboratory
Assistance
High-Impact
Dual-Use
Can improve
laboratory
efficiency, enhance
experimental
accuracy, and
reduce human
error
Can lower barriers
for conducting
complex and
dangerous
experiments by
reducing required
expertise
• Directing human usage of
specialized biological or chemical
tools/models
• Generate step-by-step laboratory
instructions
• Multimodal laboratory
troubleshooting
• Help with lab setup to minimize
failure modes
Laboratory
automation
High-Impact
Dual-Use
Can accelerate and
reduce costs of
beneficial biological
research
Can automate or
outsource key
processes that could
be exploited for
harmful purposes
• Directly using specialized biological
or chemical tools/models
• Interfacing with cloud labs with
minimal human input
• Interfacing with and automating
usage of bioinformatics software
• Writing software/code for
biological instruments
Agent
Acquisition/
Synthesis
High-Impact
Dual-Use
Can enable rapid
and efficient
production of
beneficial agents for
research and
countermeasure
development
Can provide
detailed guidance
for acquiring or
synthesizing
dangerous agents
with reduced
expertise
requirements
• Generating information for how to
acquire an agent from natural
environment
• Generating information for how to
synthesize an agent in a laboratory
• Generating information on how to
verify that an agent has expected
virulence/ pathogenicity
Design/in silico
Testing of CB
Agentsxiii
High-Impact
Dual-Use
Applications in
understanding CB
agent behavior and
developing
countermeasures
Can enable the
deliberate
modification of
pathogens to
increase their
harmful potential
• Designs that enable the
development of an agent described
in the USG Policy for Oversight of
DURC and PEPP
• Ability to accurately predict results
of new experiments

xiii This appendix describes potential risks produced by dual use foundation models; while out of scope for this
appendix, additional considerations are needed for assessment of chem-bio AI models that could enable design
and in silico testing of CB agents.

<!-- page 51 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

46

• Discovery and analysis of novel
chemical reactions
• Design of pathways to produce
toxic compounds
Weaponization/
Dissemination
Predominantly
Harmful
Very limited
legitimate
applications
Can directly enable
the weaponization
and effective
deployment of
harmful agents
• Generating information for
culturing of an agent in large
quantities
• Generating information for altering
physical properties of agent re:
formulation
• Generating information for
integration of an agent into a
dissemination system
• Generating information on agent
behavior in various environmental
conditions
• Assistance with delivery via large-
scale dissemination system
Biosecurity
Circumvention
Predominantly
Harmful
No legitimate
applications except
for assessment of
models or systems
via red-teaming
Can enable
systematic
circumvention of
critical safety and
security controls
• Technical circumvention of
synthesis or customer screening
• Generating information on
obfuscating intent / avoiding law
enforcement detection
• Generating information on
obfuscating markers useful for
bioattribution
 1

<!-- page 52 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

47

Appendix E: Application of NIST AI 800-1 to Cyber Misuse Risk    1
This appendix outlines additional considerations relevant to identifying, measuring, and mitigating risks 2
associated with the misuse of models to assist with or automate the conduct of offensive cyber 3
operations. Its goal is to complement the broader set of objectives and practices outlined in Section 5 of 4
the main document by assisting organizations in understanding domain-specific considerations that can 5
assist in applying practices for misuse risk management in this domain.xiv The considerations in this 6
appendix are primarily relevant for foundation model developers and deployers, as well as third-party 7
evaluators that work with developers and deployers to help assess cyber misuse risks; other actors’ roles 8
are discussed in Section 3 of the main document.  9
  10
E.1 Identifying Cyber Misuse Risk   11
  12
This section expands on Objective 1 ("Identify potential misuse risk") as it applies to cyber misuse risk, or 13
the risk that actors might use a model to assist with or automate malicious offensive cyber activities, 14
creating potentially significant impacts to public safety, national security, or economic security. It 15
provides considerations to assist organizations in operationalizing key practices such as establishing 16
threat profiles and assessing associated risks in the cyber domain.   17
  18
E.1.1 Establishing Threat Profiles: Actors and Scenarios  19
  20
Identifying Threat Actors: Given the diversity and number of cyber threat actors, organizations often 21
cannot predict how each individual threat actor might misuse a model, nor can they fully ignore the 22
distinctions between these actors when assessing potential model misuse.   23
  24
Instead, organizations may benefit from identifying high-level groupings or types of actors who perform 25
similar cyber activities and might therefore misuse foundation models’ capabilities in similar ways, 26
including by drawing from frameworks, standards, and concepts developed by cyber defenders to 27
categorize threat actors for the purposes of cybersecurity risk management.81 For example, based on 28
factors including “motivation”xv and “sophistication”,xvi defenders typically differentiate between nation 29
state-associated hackers and financially motivated cyber criminals.82 These groups may then be further 30
sub-divided by sophistication – for example, differentiating between groups that use advanced 31
capabilities such as zero-day exploits or custom-developed tooling versus those that rely on simpler 32
access vectors and off-the-shelf tooling83. They may also be further subdivided by motivation – for 33
example, financially motivated actors may have different goals such as ransomware and data extortion 34
versus intellectual property theft; geopolitically motivated attackers might differ in goals such as 35
espionage versus sabotage. Beyond these major profiles, other types of cyber threat actors might seek 36

xiv Note: While this appendix’s concepts align with the main NIST AI 800-1 text, some section numbers and cross-
references may not match exactly between the documents.
xv The reason or primary purpose for which a threat actor conducts offensive cyber actions. For example, see: An
Introduction to the Cyber Threat Environment (2024), Canadian Centre for Cybersecurity,
https://www.cyber.gc.ca/en/guidance/introduction-cyber-threat-environment.
xvi A concept which broadly encapsulates a group’s level of access to expertise and resources that allow them to
craft and use more bespoke and effective techniques.

<!-- page 53 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

48

to misuse model capabilities, including groups that sell offensive capabilities such as zero-days or initial 1
access,84 ideologically motivated non-state actors such as “hacktivists,” or individual actors seeking to 2
cause harm. Organizations can continually update threat actor profiles and prioritize additional 3
distinctions in an evolving manner and as more details of AI-enabled cyber threats emerge from real-4
world misuse, as described in Practice 6.1.   5
  6
Identifying Misuse Scenarios:  Next, identifying cyber scenarios that would create significant potential 7
impacts on public safety, national security, or economic security can help organizations identify 8
capabilities that present serious misuse risks. Through this process, organizations can seek to connect 9
particular model capabilities with specific, high-impact outcomes such as disruptions to critical 10
infrastructure or large-scale theft of intellectual property.   11
  12
Many high-impact cyber misuse scenarios may center around large increases in the scale or efficacy of 13
different kinds of cyber attacks, such as increases in cybercrime, espionage activity, or attacks against 14
critical infrastructure. The capabilities of foundation models could potentially increase the scale, 15
volume, or efficacy of attacks in several ways, including:  16
• Automation: Allowing threat actors to perform more attacks with the same resources by 17
automating time-intensive activities. For example, tasks such as compiling open-source 18
information for attack planning or customizing malware for particular attack targets may be 19
necessary but time-consuming for threat actors at present.  20
• Attainment: Allowing threat actors to increase their likelihood of succeeding at attacks, such as 21
by adopting more sophisticated and effective techniques. For example, the cost of zero-day 22
vulnerabilities on the gray market suggests that these capabilities are still relatively expensive to 23
develop and may be out of reach for many actors. Likewise, targeted spearphishing emails may 24
have higher success rates than generic phishing emails85 but are more time-consuming to 25
develop.  26
• Accessibility: Allowing a much wider range of actors to perform a particular kind of attack. For 27
example, a model that was proficient and reliable at coaching non-expert operators through 28
each phase of a cyber attack could potentially make the ability to perform such attacks 29
accessible to a wider group of actors.   30
  31
In addition to considering misuse scenarios based on large increases in the scale of existing activities, 32
organizations may identify other high-impact misuse scenarios by studying significant past cyber attacks 33
or wargaming with SMEs. For example, a review of cybersecurity history suggests that several of the 34
costliest historical cyberattacks were caused by worms,86 which provides evidence that this may be a 35
high-impact misuse scenario. Organizations can refine misuse scenario assessments over time by 36
integrating them with other risk management practices (such as those discussed in Section E.3); for 37
instance, misuse scenarios may inform an organization’s practices for monitoring or threat intelligence 38
gathering, and, in turn, information from ongoing monitoring can be used to prioritize and update 39
identified misuse scenarios.   40
  41
Identifying Relevant Model Capabilities: Existing cybersecurity resources, such as taxonomies of 42
attacker tactics, techniques, and procedures (TTPs),87 models of the cyber kill chain,88 and advisories on 43
specific threat actor TTPs89 can help organizations identify specific steps or activities in offensive cyber 44
operations where foundation models’ capabilities could be misused to increase a threat actor’s 45

<!-- page 54 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

49

capabilities beyond what existing tools currently provide.xvii One particularly helpful frame may be to 1
look for how a model’s capabilities may help reduce current “bottlenecks” for a particular threat actor 2
group or type of cyber activity, including those that relate to the scenarios of automation, attainment, 3
and accessibility described above.  4
  5
The increasing use of models as agents may also help automate larger offensive cyber workflows in 6
addition to assisting with completion of discrete tasks. Organizations may consider risks both from 7
capabilities at specific high-value tasks and from groups of capabilities that could enable models to 8
autonomously execute multi-step workflows or even entire attack chains. Economic models of cyber 9
crime may also be useful in identifying misuse scenarios,90 such as to identify cyber activities or targets 10
that are currently too low-return for expert human cyber operators to invest in exploiting at scale but 11
that might be more often exploited if automation with foundation models lowered the costs of doing so 12
significantly.  13
  14
To identify the particular capabilities implicated in identified misuse scenarios and to inform the design 15
of appropriate evaluations, organizations may consider:  16
• Examples of specific real-world tasks and workflows that correspond to the misuse scenario. 17
Within a general capability area, there may be important gradations in difficulty: for example, 18
within the general capability area of vulnerability discovery and exploitation, there is a 19
significant difference in both difficulty and impact between common web vulnerabilities such as 20
SQL injections and vulnerabilities in hardened software systems such as operating systems, 21
firewalls, or identity and access management services. Specific, real-world example tasks and 22
workflows can support the design of tailored capability evaluations.91  23
• How the model would be used by the threat actor in this scenario. Different threat scenarios may 24
involve the use of a model in a human uplift setting, e.g. to aid a human operator; an 25
autonomous setting, in which a model-agent system completes a particular action with little 26
human oversight; or somewhere in between. Ideally, pre- and post-deployment risk evaluations 27
can be designed to mimic this expected usage context. Likewise, evaluation design and 28
interpretation may depend on questions about the expected level of expertise of the threat 29
actor or the resources they are willing to expend to complete a particular task.   30
• The level of model performance necessary for the threat scenario. A foundation model may need 31
a particular level of accuracy, performance, or reliability for a particular threat scenario. In some 32
cyber misuse contexts, a model may be able to attempt a task many times (e.g., trying many 33
inputs to a potentially vulnerable web app or debugging an exploit against a local target) and in 34
others a model might need high accuracy on each attempt (e.g., identifying vulnerabilities that 35
must then be explored and validated by a human operator, or using an exploit against a closely 36
monitored remote target). There are varied ways to define and measure performance for a 37
particular task, but two common approaches include:   38

xvii Threat actors currently use a variety of software tools to automate parts and processes of conducting cyber
attacks (for example, see Ransomware Rebounds (2024). Google. https://cloud.google.com/blog/topics/threat-
intelligence/ransomware-attacks-surge-rely-on-public-legitimate-tools); organizations may consider these existing
tools in identifying existing gaps and workflows where AI capabilities could provide uplift above and beyond what
is already available through existing software-based tools.

<!-- page 55 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

50

o Directly defining an objective measure of the model's ability to obtain a binary 1
or continuous outcome – for example, whether a model can successfully 2
identify and exploit a specific kind of vulnerability.  3
o Defining a way to compare the performance of the model to the performance of 4
humans – for example, whether a model can write a phishing email that is more 5
persuasive than a phishing email written by an expert human.  6
• The types of real-world defenses with which a model might interact in a threat scenario. 7
Defensive systems, from intrusion detection systems to email filters, will play a key role in 8
mediating the potential cyber misuse risks of model capabilities. Considering the dynamics of 9
these interactions – including a model’s adaptability to overcome such defenses, and how 10
defenses might adapt in turn – can help inform risk assessments and the design of appropriate 11
evaluations.   12
  13
E.1.2 Risk Assessment  14
  15
Best practices for cyber misuse risk assessment are still nascent. Existing frameworks for cyber risk 16
assessment are primarily intended for assessment of cyber risks to an organization; however, these 17
documents offer approaches to selecting and operationalizing qualitative and quantitative cyber risk 18
assessments that organizations may adapt in seeking to assess cyber misuse risks.92  19
  20
A widely used formula for quantitative risk assessments, both in cyber and in other domains, is to 21
multiply the potential impacts of a negative outcome times the likelihood of such an event occurring. 22
This approach may be well-suited for cyber misuse scenarios that focus on a single, high-impact event, 23
but less tractable for scenarios that involve increasing the scale of current cyber activities across the 24
ecosystem, where modelling the likelihood of each individual event may be prohibitively challenging. 25
Instead, organizations may adapt this approach to model how a model capability might increase current 26
or baseline risks associated with particular kinds of cyber activity.   27
 28
Estimating Baseline Risk: Rather than separately estimating the impact and likelihood of cyber events, 29
organizations may estimate a baseline level of risk based on the current costs or harms created by a 30
particular category of cyber activity. A range of actors already aggregate and report data about cyber 31
attacks and associated costs, which can help inform these estimates.93 Organizations should consider 32
using data and estimation techniques to assess costs that are both comprehensive and specific to the 33
threat profile. Assessing comprehensive costs for certain kinds of cyber activities may require 34
considering not only direct losses, but broader costs such as indirect losses (e.g., revenue loss due to 35
downtime or declining consumer trust) and the costs of implementing defenses.94 Some important 36
harms may be challenging to estimate in dollar amounts, such as harms to US national security interests 37
or privacy harms to individuals. Organizations might seek to estimate a dollar value for these harms 38
using related data sources (e.g., on the costs that companies or governments currently pay to prevent 39
these harms95) or use non-monetary variables to represent current baselines. In general, where high-40
quality data on baseline impacts is unavailable or where available data suggests a large range of possible 41
values, organizations could use other processes to generate and refine estimates such as soliciting and 42
aggregating independent expert estimates.  43
  44
Estimating Misuse Risk: After estimating baseline risk for a category of cyber activities, organizations 45
might estimate how a particular model capability (or a combination of capabilities) could modulate this 46

<!-- page 56 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

51

risk. There is not yet consensus on a single best approach to such risk modelling. One example could be 1
using concepts of automation, attainment, and accessibility to estimate how a particular capability 2
might scale threat actors' baseline output: for example, a model capability that provided automation 3
could scale output by increasing the number of attacks that the average threat actor can attempt in a 4
given time period; a capability that increased attainment could scale output by increasing the success 5
rate of the average attack attempt; or a capability that increased accessibility could scale output by 6
increasing the overall number of threat actors attempting attacks. For example, a model capability that 7
allowed the average threat actor to automate a task that currently takes 20% of operation time could 8
theoretically increase the number of attacks each actor attempts in a given time period by 25% 9
(assuming perfect efficiency), resulting in a new estimated impact of 1.25*(baseline). Then, the misuse 10
risk associated with that model capability would be given by the difference between the new estimated 11
risk and the baseline risk, or 0.25*(baseline).  12
  13
In reality, even “simple” relationships like the impacts of automation are unlikely to have purely linear 14
effects because of relationships between variables – for example, increasing the average number of 15
attacks that attackers can perform in a given time period might have sublinear effects because each 16
marginal new target may be more difficult to compromise than the previous average, or superlinear 17
effects because cheaper attacks could become appealing to a larger number of attackers. Organizations 18
can seek to identify and to correct for the direction of these effects or to use modelling approaches that 19
account for these relationships in their final estimates.   20
  21
Estimating Misuse Risk from Rare, High-Impact Events: For cyber scenarios that center around 22
infrequent but high-consequence events, organizations might use a more traditional risk estimation 23
formula such as impact multiplied by likelihood – or, to estimate marginal risk, impact multiplied by the 24
increase in likelihood as the result of the model capability. Estimates of the potential impact and 25
likelihood (with and without the model capability) could be created by aggregating multiple 26
independent expert assessments or drawing from case studies of significant past cyber attacks.   27
  28
Transparency: The process of estimating the potential impacts of cyber capability misuse is still nascent 29
and requires organizations to grapple with significant uncertainty. Public transparency about this 30
process and its results can enable other parties – in particular the broader community of cybersecurity 31
defenders, experts, and researchers – to offer feedback on specific assumptions and generally facilitate 32
collaboration towards a stronger consensus on methodological best practices. Where possible, 33
organizations might share full insights into their process and resulting estimates; where these analyses 34
are too sensitive to share in their entirety, publishing information about risk assessment methodology, 35
data sources, or open questions could still be useful to the broader field, as described in the 36
documentation associated with the Objectives above and in Objective 7 in particular.  37
  38
E.1.3 Key Challenges & Opportunities for Identifying Cyber Misuse Risk   39
• Cyber-relevant model capabilities span a diversity of activities, actors, and contexts. A single 40
cyber operation may implicate diverse skillsets, activities, and expertise, from the ability to craft 41
a persuasive phishing email to specific technical knowledge of the features of networking 42
protocols or endpoint detection and response software. These activities vary across actors from 43
“script kiddies” to well-resourced “advanced persistent threats”, and actors’ varied motivations, 44
resources, and needs shape how they might misuse (and benefit from the misuse of) model 45
capabilities. The cybersecurity field has a significant body of work characterizing this threat 46

<!-- page 57 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

52

environment for defenders; by building atop these foundations and engaging with the broader 1
cybersecurity community, organizations can ground their practices in considerable prior work.   2
• Foundation model-enabled cyber threats will not be static. As defensive measures improve, 3
threat actors will adapt their methods and seek new paths to exploitation, creating a moving 4
target for cyber risk assessments. Organizations may need to continually update their 5
understanding of attacker tradecraft and model capabilities, leverage threat intelligence, and 6
refine their risk assessments in an iterative manner to keep pace. However, this ongoing process 7
will create significant opportunities for organizations to closely integrate risk assessments with 8
risk management practices, and to learn from and contribute back to the broader cyber defense 9
ecosystem over time.  10
• Cyber is a domain where the potential for model-enabled scale may be particularly powerful. 11
Foundation models’ advantages with respect to automation may be particularly impactful in 12
digital contexts like cyber, where activities – once automated – have the potential to be scaled 13
arbitrarily without a bottleneck on human operators taking actions in the physical world. 14
Automation-enabled scaling of particular cyber attack techniques or workflows could increase 15
attackers’ efficacy, alter the economics of offense and defense in the cyber ecosystem, and 16
overwhelm defenders’ resources.  Organizations should consider the effects of scale in 17
identifying high-impact scenarios for misuse of cyber-capable models.    18
  19
E.2 Evaluating Cyber Capabilities  20
Building on Objective 4 (“Measure the Risks of Misuse”) and the measurement characteristics outlined 21
in Appendix C, this section provides considerations for measuring cyber misuse risks in the context of 22
pre- or post-deployment model evaluations, including an overview of evaluation types in the cyber 23
domain and specific methodological considerations for cyber capabilities evaluations.   24
  25
E.2.1 Cyber Evaluation Types  26
  27
Direct Measurement: The digital nature of the cyber domain permits organizations to directly measure 28
many cyber capabilities through evaluations in which models interact with real or realistic information 29
systems and resources in isolated, simulated, or otherwise non-harmful contexts. For example, 30
evaluators could curate a collection of vulnerable open source codebases96 or codebases with 31
synthetically injected vulnerabilities97 to measure a model’s ability to identify vulnerabilities, or use 32
“cyber ranges” or synthetic network environments to test whether a model can take actions such as 33
establishing persistence, moving laterally, or evading common defenses.   34
  35
Direct measurements can be designed as automated evaluations, in which a model or model-agent 36
system’s performance is automatically scored according to pre-defined criteria. In the cyber context, 37
examples include:  38
• Environmental objectives, such as capture-the-flag style evaluations,xviii in which a model-agent 39
system interacts with a vulnerable computer system or resource to find a hidden “flag” and 40
passes or fails the task based on whether it successfully submits the flag within a certain number 41
of messages.   42

xviii Note that capture-the-flag style evaluations is not necessarily synonymous with evaluations based on challenges from
real-world “Capture the Flag” competitions; tasks designed specifically for the purposes of AI evaluation may still use a
capture-the-flag style scoring mechanism for ease of automatic grading.

<!-- page 58 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

53

• Ground truth scoring, such as for vulnerability identification evaluations where model-identified 1
vulnerabilities are compared to a known ground truth of vulnerabilities present in a particular 2
code sample.98   3
 4
Designs for automated direct measurements are less mature in capability areas like social engineering, 5
where the need to assess interactions with humans creates additional methodological challenges.   6
Direct measurement on real cyber tasks without automatic scoring – for example, having an expert use a 7
model to try to complete a real cyber task – can provide valuable evidence about model capabilities, 8
especially in the context of use by a human operator. However, standardization of best practices for 9
qualitative judgements of model performance and methods for controlling for the effects of operator 10
contributions are still nascent. Thus, these evaluations may be useful for exploring areas of capability 11
and risk but less suited for use in performance comparisons.   12
  13
Performance Comparisons: Performance comparisons help contextualize cyber capability 14
measurements in comparison to existing models or human experts to support marginal risk assessment. 15
For example, challenges from university- or professional-level “Capture the Flag” competitions are 16
widely used as cyber benchmarks99 because they provide self-contained environments to test 17
vulnerability discovery and exploitation skills. These challenges differ from real-world vulnerabilities – in 18
that they involve smaller and simpler artifacts and are designed to be solvable, entertaining puzzles – 19
preventing direct mapping from models' performance on these challenges to estimates of capability at 20
real-world vulnerability discovery and exploitation. However, because these challenges require similar 21
skills, they can be useful in performance comparisons to existing models or to human experts: if a new 22
model underperforms publicly available models on CTF challenges, it provides some evidence that it is 23
unlikely to be significantly more capable at real-world vulnerability discovery; if a model cannot solve 24
CTFs that take human experts a relatively short amount of time, it provides some evidence that the 25
model is unlikely to succeed at real-world vulnerability discovery tasks that take human experts a much 26
greater amount of time. For these kinds of performance comparisons, organizations should validate key 27
assumptions about the relationship between the evaluation tasks and the real-world tasks of concern, 28
such as by soliciting opinions from multiple independent experts.   29
  30
E.2.2 Considerations for Cyber Evaluations  31
  32
Breadth and Depth: When selecting evaluations for a particular cyber capability, organizations may 33
consider both breadth and depth of the evaluations:  34
• Breadth: whether evaluation tasks comprehensively cover the distribution of real-world tasks of 35
concern, especially if there is significant variety in these tasks. For example, assessing a model’s 36
ability to find memory management vulnerabilities may provide weak evidence about its ability 37
to find design flaws in identity and access management infrastructure and vice versa.   38
• Depth: whether a benchmark has headroom – room for a model to improve its score without 39
saturating the benchmark – and gradations of difficulty sufficient to track progress in model 40
capabilities over time. Organizations may be able to add additional gradations in difficulty 41
through evaluation design, for example, by varying the amount of information provided to a 42
model about the vulnerability that it needs to exploit in a capture-the-flag challenge. Human 43
baselines (e.g., measures of how long the tasks in a benchmark take human experts to 44
complete) can help evaluators assess the relative difficulty of different tasks as well as support 45
in conducting performance comparisons.  46

<!-- page 59 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

54

 1
Elicitation: Especially for agent-based evaluations like capture the flag-style evaluations, elicitation is a 2
key methodological consideration. Elicitation refers to efforts to maximize the performance of a model 3
on a task through methods such as improving prompts, using more performant agent scaffolds, or fine-4
tuning. In the cyber evaluation context, elicitation can help ensure that a model is measured on tasks in 5
a way that comparably effective to how it could be used by threat actors in the misuse scenario the 6
evaluation is designed to measure. Research results and observations of the performance of tailored 7
agents for cyber applications suggest that elicitation can significantly increase model performance.100  8
• Organizations may use a process for elicitation prior to or during an evaluation to select an 9
agent scaffold that is optimized for both the model being evaluated and the specific evaluation 10
tasks. Organizations can use a “development set” of similar tasks that is separate from the “test 11
set” of evaluation tasks to experiment with agent architectures and prompts, review transcripts 12
to address causes of failure, and select the best-performing agent scaffold.101  13
• Access to appropriate cybersecurity tools and utilities such as a code interpreter, debugger, 14
decompilation tool, file editing tool, or web browsing tool may significantly improve agent 15
performance on cyber tasks.102 Useful practices may include providing agents with tools 16
comparable to what a human expert would use to complete a task, reviewing task transcripts to 17
identify tools that agents attempt to use during task runs and pre-installing them in the agent 18
environment, and informing agents of available tools in initial prompts.   19
• Organizations can form evidence-based hypotheses about the magnitude of potential post-20
release performance gains through additional elicitation and factor this into assessments of 21
model capability. If a developer believes that existing agent scaffolds may not be well-suited for 22
the evaluated model, such as if it is paradigmatically different from previous state-of-the-art 23
models, they may use a larger estimate.  24
• Organizations can observe how models are applied and customized to real-world cyber tasks 25
and applications in practice and seek to use similar designs and methods during evaluations.   26
  27
Running Cost-Aware Evaluations: Evaluators may consider documenting or controlling for costs when 28
running cyber evaluations, either to approximate the costs that a threat actor might be willing to pay for 29
a particular misuse case (for direct measurement) or to support performance comparisons between 30
models or with human experts. There are several ways that additional inference compute can improve 31
model performance, including allowing models longer chains of thought or more tool calls, or running 32
more separate trials and combining the results such as by taking a majority vote or using the best 33
outcome (for tasks like vulnerability discovery, where it is possible to verify success).103 Organizations 34
may use these methods to help equalize inference costs across models as appropriate.  35
 36
Contamination: Since many cyber evaluations are based on public data, evaluators should be cognizant 37
of contamination risks. Contamination could arise not only from public cyber benchmarks in training 38
data but also from other publicly available information about evaluation tasks – such as descriptions of 39
past CVEs or write-ups of CTF challenges – present in training data or queried by an internet-connected 40
agent at evaluation time. Evaluators may seek or develop benchmarks that rely on private data and use 41
held-out test sets to reduce the risk of contamination, and organizations should avoid overlap between 42
data used to train a model and data used in capability evaluations, including by respecting canary 43
strings, as described in Practice 4.1104 44
 45

<!-- page 60 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

55

Standardization and Transparency: Organizations may consider how to design and document cyber 1
evaluations to allow for consistent comparison over time and across different models. Standardization 2
of metrics and testing procedures, documentation of key methodological decisions, and reporting of 3
supporting results such as ablation experiments for elicitation techniques can support the cross-4
comparison and replication of results within and outside of an organization over time.    5
  6
E.2.3 Key Challenges and Opportunities for Measuring Cyber Capabilities  7
  8
• Models will be applied and customized to cyber tasks in ways beyond what can be measured 9
in a time-bound evaluation setting. Attackers and defenders are constantly evolving, 10
experimenting, and engineering to gain the upper hand in the cyber domain. Once a model is 11
released, both specific threat actors and the broader cybersecurity community will experiment 12
in applying it to new cybersecurity tasks and may improve its performance through customized 13
scaffolds and new methods of elicitation. Evaluators cannot realistically recreate this 14
decentralized development process within the timebound context of an evaluation, creating 15
challenges in mapping from evaluation results to estimates of real-world capability; better 16
methods for estimating the size of this effect are still needed.  Evaluators can gain valuable 17
insight from observing applications of deployed models, which can help inform analysis of cyber 18
misuse risks and improve methods for capability measurement.  19
• Designs, datasets, and standard tooling for cyber evaluations are still being developed. While 20
the digital nature of the cyber domain has advantages in allowing the direct evaluation of 21
models on a variety of real or realistic cyber tasks, the creation of datasets, tools, and resources 22
for cyber evaluations is still in its early days. Benchmarks have been publicly released that are 23
comprised of CTF challenges or based on real vulnerability data have been publicly released, but 24
there are fewer purpose-built benchmarks for simulating entire networks and attack chains or 25
evaluating capabilities in social engineering. Standard frameworks exist for running agent-based 26
evaluations105 but they are not universally adopted. And additional auxiliary tooling, such as 27
tooling to assist in performing elicitation or reviewing task transcripts for causes of failure, is still 28
being developed.   29
  30
  31
E.3 Managing and Mitigating Cyber Misuse Risk  32
  33
This section expands on Objective 2 ("Plan for Managing Misuse Risk"), Objective 5 (“Mitigate Misuse 34
Risk Before Deployment”), and Appendix B (“Example Safeguards Against the Misuse of Foundation 35
Models”). It outlines some key considerations in operationalizing mitigations for cyber misuse risks and 36
calls attention to several as-yet unsolved challenges in this area.   37
  38
E.3.1 Considering Dual-Use Dynamics in Risk Management  39
  40
Reducing Compliance with Harmful Requests: The dual-use nature of many cyber tools and the close 41
resemblance – in the absence of additional context about a user’s intent or authorization – between 42
malign and benign cyber tasks creates challenges for mitigations like safety training for refusals or 43
auxiliary request filtering that aim to reduce compliance with harmful requests at inference time. A 44
threat actor might disguise a request to craft a phishing email as assistance in drafting an outreach 45

<!-- page 61 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

56

email, ask a model to identify vulnerabilities in code in the guise of a developer seeking to address them, 1
or request distinct commands or pieces of code that are malicious only when combined. Organizations 2
may not be able to fully prevent compliance with such misuse requests without also blocking certain 3
benign use cases. While reducing helpfulness with overtly malicious cyber tasks may still be an 4
important component of broader cyber misuse risk management, organizations may need to use these 5
approaches in concert with other mitigations.   6
 7
User Accounts: For models offered through an API, requiring user accounts and monitoring longer-8
running usage patterns for signs of offensive cyber misuse can allow organizations to identify and block 9
usage by cyber threat actors.106 However, this monitoring may still face similar challenges in 10
differentiating cyber misuse from legitimate use cases such as security research.   11
  12
Staged Releases and User Vetting: For highly cyber-capable models, organizations may employ staged 13
releases to advantage defenders’ access to a model ahead of attackers’: for example, a developer 14
could make a model with significant vulnerability discovery capabilities available to verified 15
organizations and developers before allowing access by unverified users, allowing them to use the 16
model to find and fix some vulnerabilities before attackers can use the model to discover and exploit 17
them. However, staged release strategies require realism about the broader cybersecurity ecosystem: 18
adoption and integration of defensive tools takes time, slow patching is a known challenge in 19
cybersecurity,107 and significant numbers of legacy systems can no longer receive upgrades and security 20
patches even if vulnerabilities are found.108 21
  22
Modifying Outputs to Reduce Misuse Potential: In certain cases, organizations may be able to modify 23
model outputs to asymmetrically reduce the utility of the outputs for threat actors without needing to 24
differentiate between malign and benign uses at inference time. For example, placing a visible 25
watermark or indicator on an AI-generated video of a person’s likeness could make it less useful for 26
social engineering attacks.109  27
  28
E.3.2 Using Identified Threat Actors to Inform and Evaluate Risk Mitigations  29
  30
In the cyber context in particular, threat actors who might wish to misuse a model for cyber offense may 31
be willing and able to use offensive cyber techniques to gain access to models and circumvent 32
protections for the purposes of misuse. Thus, information security measures and adversarial testing may 33
play significant roles in the cyber misuse management strategies of developers and deployers.  34
  35
Organizational Security Practices: Organizations cyber misuse risk management plans should include 36
consideration of whether organizational information security measures are sufficient to prevent 37
unauthorized access to models by identified cyber misuse actors (i.e., potentially up to and including 38
nation-state threat actors) wherever unauthorized access would subvert key assumptions about misuse 39
risk management, such as that model access is controlled through an API. Beyond employing general, 40
industry-standard cybersecurity best practices, organizations may consider additional security practices 41
specific foundation models, as described in Practices 3.1 and 3.2. 42
 43
Protections for Deployed Models: When applying misuse risk mitigations for deployed models such as 44
user account-level protections or measures to reduce model compliance with malign requests, 45

<!-- page 62 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

57

organizations should evaluate the efficacy of these measures considering the resources and 1
sophistication of the adversaries they are intended to protect against.   2
 3
Red-Team Testing: Traditional cybersecurity red-team testing of organizational networks and 4
deployment infrastructure, as well as AI-specific adversarial red-teaming of model safeguards, can assist 5
in validating the robustness of these measures and closing exploitable gaps.   6
 7
E.3.3 Refining Risk Management Based on Real-World Evidence  8
  9
Cybersecurity is a fast-evolving and adversarial environment, and organizations will receive significant 10
evidence based on real-world use of their foundation models and proxy models that can be used as a 11
part of risk management practices.   12
  13
Monitoring for Misuse: If offered through an API, organizations can monitor deployed models for 14
misuse to apply mitigations such as restricting user accounts or updating systems to reduce compliance 15
with malicious requests. Regardless of deployment strategy, organizations can monitor other sources of 16
public information such as forums, news reports, and cybersecurity advisories for evidence of offensive 17
cyber misuse of their foundation models or similar models. This information can be useful for updating 18
safeguards for previously released models and for refining risk assessments, measurements, and 19
mitigations for future models.   20
  21
Tracking Cyber Capabilities and Applications: Organizations can stay up to date on the work of other 22
companies and researchers to understand how users have customized and applied models for real-23
world cyber tasks and applications, including where scaffolds or other methods of elicitation have 24
improved model performance on these types of tasks. This information can refine assessments of model 25
capability in real-world settings as compared to measurements in pre-deployment evaluations and feed 26
into the design of future evaluations such as by providing new methods of elicitation.  27
  28
Planning for Adaptive Defenses: Organizations can seek to prioritize the development of layered and 29
adaptable defensive mechanisms that are designed to be updated over time based on evolving 30
information about the threat landscape and attacker methods. For example, organizations might create 31
organizational structures and technical methods to rapidly update misuse detection tools based on 32
ongoing threat intelligence, or develop AI systems to assist in rapidly identifying and responding to new 33
patterns of misuse.   34
  35
Transparency: Publishing information on identified cyber misuse of models can assist the broader 36
ecosystem in understanding real-world cyber misuse risks. Best practices for detecting and disrupting 37
cyber misuse of foundation models are still nascent, and sharing methodologies, information, or tools 38
relating to cyber misuse detection – with the broader public where possible without compromising their 39
efficacy, and with smaller and more trusted groups for more sensitive information – can assist other 40
organizations in maturing their own detection and disruption methods.   41
 42
 43
  44

<!-- page 63 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

58

E.3.4 Key Challenges and Opportunities for Mitigating Cyber Misuse Risk  1
  2
• Dual-use dynamics are fundamental to cyber misuse risk management but not yet fully 3
characterized. The dynamics of the offense-defense interplay in cyber mean that most 4
capabilities will be, in some sense, dual use. However, the specific dynamics of this interplay, 5
including whether and how defensive uses can counteract offensive ones, will vary based on 6
capabilities and the broader characteristics of the cyber ecosystem. While early theoretical work 7
has explored this space,110 further study is needed. These dynamics will challenge organizations 8
to design mitigations that can reduce the misuse potential of a model without impacting benign 9
use cases but may also create opportunities to deploy capabilities for defensive purposes.  10
• Reliably differentiating cyber misuse from legitimate use cases may be challenging. The use of 11
a model to write software, draft emails, and even to actively probe systems may not be easily 12
distinguished between beneficial activities like security research and threat actor misuse 13
without additional context, presenting challenges for designing and implementing mitigations 14
such as refusals, request filtering, and user account-level interventions. Monitoring additional 15
sources of public information and providing reporting mechanisms may help provide some 16
additional context to distinguish security research from offensive cyber operations, and further 17
transparency around practices and open questions in this area can assist in the maturation of 18
consensus best practices.111  19
• Evolving attacker techniques will require adaptive defenses. Threat actors are likely to 20
continually adapt their techniques to circumvent established safeguards, rendering once-21
effective controls quickly outdated, and organizations may need to continually evolve their risk 22
mitigations in tandem with attacker methods. Organizations can seek to create adaptive 23
mitigations that are designed to be updated over time, based on feedback loops from real-world 24
incidents and threat intelligence, to help maintain the effectiveness of safeguards over time.   25

1 Memorandum on Advancing the United States’ Leadership in Artificial Intelligence; Harnessing Artificial
Intelligence to Fulfill National Security Objectives; and Fostering the Safety, Security, and Trustworthiness of
Artificial Intelligence (2024). https://www.whitehouse.gov/briefing-room/presidential-
actions/2024/10/24/memorandum-on-advancing-the-united-states-leadership-in-artificial-intelligence-harnessing-
artificial-intelligence-to-fulfill-national-security-objectives-and-fostering-the-safety-security/.
2 Anwar, U. et al., (2024) Foundational Challenges in Assuring Alignment and Safety of Large Language Models.
arXiv. https://arxiv.org/pdf/2404.09932. For information on the rate of progress of foundation models, see Maslej,
N. et al., (2024) The AI Index 2024 Annual Report. AI Index Steering Committee, Institute for Human-Centered AI,
Stanford University. https://aiindex.stanford.edu/wp-content/uploads/2024/05/HAI_AI-Index-Report-2024.pdf;
Ho, A. et al., (2024) Algorithmic progress in language models. arXiv. https://arxiv.org/abs/2403.05812; and Sevilla,
J. et al., (2024) Training Compute of Frontier AI Models Grows by 4-5x per Year. Epoch AI.
https://epochai.org/blog/training-compute-of-frontier-ai-models-grows-by-4-5x-per-year.
3 Vogel, M. et al., (2024) Findings & Recommendations: AI Safety. National AI Advisory Committee.
https://ai.gov/wp-content/uploads/2024/06/FINDINGS-RECOMMENDATIONS_AI-Safety.pdf.
4 Executive Order 14110 on the Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence (2023)
The White House. https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-
on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/.
5 Dual-Use Foundation Models with Widely Available Model Weights Report (2024). National Telecommunications
and Information Administration. https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-
model-weights-report ; Kapoor, S. et al., (2024) Position: On the Societal Impact of Open Foundation Models.

<!-- page 64 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

59

Proceedings of the 2024 International Conference on Machine Learning.
https://openreview.net/pdf?id=jRX6yCxFhx.
6 Blueprint for an AI Bill of Rights (2022) The White House. https://www.whitehouse.gov/ostp/ai-bill-of-rights/.
7 NIST AI 600-1 AI Risk Management Framework: Generative Artificial Intelligence Profile. National Institute of
Standards and Technology. https://airc.nist.gov/docs/NIST.AI.600-1.GenAI-Profile.ipd.pdf.
8 Srikumar, M. et al., (2024) Risk Mitigation Strategies for the Open Foundation Model Value Chain. Partnership on
AI. https://partnershiponai.org/resource/risk-mitigation-strategies-for-the-open-foundation-model-value-chain/;
Heim, L. et al., (2024) Governing Through the Cloud: The Intermediary Role of Compute Providers in AI Regulation.
arXiv. https://arxiv.org/pdf/2403.08501; and Gorwa, R. et al. (2023) Moderating Model Marketplaces: Platform
Governance Puzzles for AI Intermediaries. arXiv. https://arxiv.org/abs/2311.12573.
9 Ibid.
10 Constanza-Chock, S. et al., (2022) Who Audits the Auditors? Recommendations from a field scan of algorithmic
auditing ecosystem. Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency.
https://dl.acm.org/doi/abs/10.1145/3531146.3533213.; Cen, S. et al., (2024) AI Supply Chains. SSRN.
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4789403.
11 Narayanan, A. and Kapoor, (2024) AI safety is not a model property. AI Snake Oil.
https://www.aisnakeoil.com/p/ai-safety-is-not-a-model-property.; T. et al., (2023) AlphaFold predictions are
valuable hypotheses and accelerate but do not replace experimental structure determination. Nature.
https://www.nature.com/articles/s41592-023-02087-4.
12 S. et al., (2024) Position: On the Societal Impact of Open Foundation Models. Proceedings of the 2024
International Conference on Machine Learning. https://openreview.net/pdf?id=jRX6yCxFhx.
13 Hoffmann, J. et al., (2022) Training Compute-Optimal Large Language Models. Proceedings of the 2022
Conference on Neural Information Processing Systems. https://dl.acm.org/doi/10.5555/3600270.3602446.
14 Besiroglu, T. et al., (2024) Chinchilla Scaling: A replication attempt. arXiv. https://arxiv.org/pdf/2404.10102.
15 Anwar, U. et al., (2024) Foundational Challenges in Assuring Alignment and Safety of Large Language Models.
arXiv. https://arxiv.org/pdf/2404.09932.
16 Upadhayay, B. and Behzadan, V. (2024) Sandwich Attack: Multi-language Mixture Adaptive Attack on LLMs.
arXiv. https://arxiv.org/abs/2404.07242; Zou, A. et al., (2023) Universal and Transferable Adversarial Attacks on
Aligned Language Models. arXiv. https://arxiv.org/pdf/2307.15043.
17Adapted from OECD Digital Economy Papers, (2022) OECD Framework for the Classification of AI Systems. OECD.
https://www.oecd.org/en/publications/oecd-framework-for-the-classification-of-ai-systems_cb6d9eca-en.html.
18 Kapoor, S. et al., (2024) Position: On the Societal Impact of Open Foundation Models. Proceedings of the 2024
International Conference on Machine Learning. https://openreview.net/pdf?id=jRX6yCxFhx; and Mouton, C. et al.,
(2024) The Operational Risks of AI in Large-Scale Biological Attacks. RAND.
https://www.rand.org/pubs/research_reports/RRA2977-2.html.
19 Bernardi, J. et al., (2024) Societal Adaptation to Advanced AI. arXiv. https://arxiv.org/abs/2405.10295.
20 NIST AI 100-1 AI Risk Management Framework. National Institute of Standards and Technology.
https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf; NIST AI 600-1 AI Risk Management Framework: Generative
Artificial Intelligence Profile. National Institute of Standards and Technology.
https://airc.nist.gov/docs/NIST.AI.600-1.GenAI-Profile.ipd.pdf; and NIST SP 800-30 Guide for Conducting Risk
Assessments. National Institute of Standards and Technology. https://csrc.nist.gov/pubs/sp/800/30/r1/final.
21 Nevo, S., et al., (2024) Securing AI Model Weights. RAND.
https://www.rand.org/pubs/research_reports/RRA2849-1.html.
22 NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations (2020). National
Institute of Standards and Technology. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final; NIST SP 800-218A:
Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community
Profile (2024). National Institute of Standards and Technology. https://csrc.nist.gov/pubs/sp/800/218/a/ipd.
23 Ibid.

<!-- page 65 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

60

24 Carlini, N. et al., (2024) Stealing Part of a Production Language Model. arXiv, https://arxiv.org/pdf/2403.06634;
Nevo, S., et al., (2024) Securing AI Model Weights. RAND. https://www.rand.org/pubs/research_reports/RRA2849-
1.html.
25 Casper, S. et al., (2024) Black-Box Access is Insufficient for Rigorous AI Audits. arXiv.
https://arxiv.org/pdf/2401.14446.
26 Bran, A. et al., (2024) Augmenting large language models with chemistry tools. Nature.
https://www.nature.com/articles/s42256-024-00832-8; Davidson, T. et al., (2023) AI capabilities can be
significantly improved without expensive retraining. arXiv. https://arxiv.org/pdf/2312.07413; Measuring the
impact of post-training enhancements. METR. https://metr.github.io/autonomy-evals-guide/elicitation-gap/.
27 Jin, H. et al., (2024) JailbreakZoo: Survey, Landscapes, and Horizons in Jailbreaking Large Language and Vision-
Language Models. arXiv. https://arxiv.org/pdf/2407.01599.
28 O’Brien, J. et al., Deployment Corrections: An incident response framework for frontier AI models. Institute for AI
Policy and Strategy. https://arxiv.org/pdf/2310.00328.
29 Cattell, S. et al., (2024) Coordinated Flaw Disclosure for AI: Beyond Security Vulnerabilities. arXiv.
https://arxiv.org/abs/2402.07039; for an example of researchers pursuing coordinated disclosure practices, see
Nasr, M., et al., (2023) Scalable Extraction of Training Data from (Production) Language Models. arXiv.
https://arxiv.org/pdf/2311.17035.
30 Longpre, S. et al., (2024) A Safe Harbor for AI Evaluation and Red-Teaming. arXiv.
https://arxiv.org/pdf/2403.04893.
31 Bucknall, B. et al., (2023). Structured Access for Third-Party Research on Frontier AI Models. Center for the
Governance of AI. https://www.governance.ai/research-paper/structured-access-for-third-party-research-on-
frontier-ai-models.
32 Wan, S. et al., (2024) Bridging the Gap: A Study of AI-based Vulnerability Management between Industry and
Academia. arXiv. https://arxiv.org/abs/2405.02435.
33 Phuong, M. et al., (2024) Evaluating Frontier Models for Dangerous Capabilities. arXiv.
https://arxiv.org/pdf/2403.13793; Anthropic (2024) Claude 3.5 Sonnet Model Card Addendum. Anthropic.
https://www-
cdn.anthropic.com/fed9cc193a14b84131812372d8d5857f8f304c52/Model_Card_Claude_3_Addendum.pdf;
OpenAI (2023) GPT-4 System Card. OpenAI. https://cdn.openai.com/papers/gpt-4-system-card.pdf
34 Bommasani, R. et al., (2024) The Foundation Model Transparency Index v1.1: May 2024. arXiv.
https://arxiv.org/pdf/2407.12929.
35 Longpre, S. et al., (2023). The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution
in AI. arXiv. https://arxiv.org/abs/2310.16787.
36 Voluntary AI Commitments. White House. https://www.whitehouse.gov/wp-
content/uploads/2023/09/Voluntary-AI-Commitments-September-2023.pdf; Bommasani, R. et al., (2024) The
Foundation Model Transparency Index v1.1: May 2024. arXiv. https://arxiv.org/pdf/2407.12929.
37 Voluntary AI Commitments (2023). The White House. https://www.whitehouse.gov/wp-
content/uploads/2023/09/Voluntary-AI-Commitments-September-2023.pdf.; Hiroshima Process International
Code of Conduct for Organizations Developing Advanced AI Systems (2023). G7 2023 Hiroshima Summit.
https://www.soumu.go.jp/hiroshimaaiprocess/pdf/document05_en.pdf.; Frontier AI Safety Commitments (2024).
AI Seoul Summit 2024. https://www.gov.uk/government/publications/frontier-ai-safety-commitments-ai-seoul-
summit-2024/frontier-ai-safety-commitments-ai-seoul-summit-2024.
38 McGregor, S. (2020) Preventing Repeated Real World AI Failures by Cataloging Incidents: The AI Incident
Database. arXiv. https://arxiv.org/pdf/2011.08512.
39 One example of such a format is the OECD AI Incidents Monitor (AIM).
40 Turri, V. et al., (2023) Why We Need to Know More: Exploring the State of AI Incident Documentation Practices.
AAAI/ACM Conference on AI Ethics and Society. https://doi.org/10.1145/3600211.3604700.
41 The term “artificial intelligence” or “AI” has the meaning set forth in 15 U.S.C. 9401(3).
42 Executive Order 14110.

<!-- page 66 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

61

43 Executive Order 14110.
44 NIST AI 100-1 AI Risk Management Framework. National Institute of Standards and Technology.
https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf.
45  Thiel, D., et al., (2023) Identifying and Eliminating CSAM in Generative ML Training Data and Models. Stanford
Digital Repository. https://purl.stanford.edu/kh752sm9123.
46 Yuan Y. et al., (2024) Refuse Whenever You Feel Unsafe: Improving Safety in LLMs via Decoupled Refusal
Training. arXiv. https://arxiv.org/abs/2407.09121 .
47 Henderson, P. et al., (2022) Self-Destructing Models: Increasing the Costs of Harmful Dual Uses of Foundation
Models. arXiv. https://arxiv.org/pdf/2211.14946.
48 https://www.ingentaconnect.com/contentone/hsp/airwa/2024/00000003/00000001/art00005; Lynch, A. et al.,
(2024) Eight Methods to Evaluate Robust Unlearning in LLMs. arXiv. https://arxiv.org/pdf/2402.16835.
49 Bommasani, R. (2023) Ecosystem graphs: The social footprint of foundation models.
https://arxiv.org/abs/2303.15772.
50 Seger, E. et al., (2024) Open-Sourcing Highly Capable Foundation Models.  https://cdn.governance.ai/Open-
Sourcing_Highly_Capable_Foundation_Models_2023_GovAI.pdf
51  Qi, X. et al., (2024) Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend
To! arXiv. https://arxiv.org/pdf/2310.03693.
52 Kapoor, S. et al., (2024) Position: On the Societal Impact of Open Foundation Models. Proceedings of the 2024
International Conference on Machine Learning. https://openreview.net/pdf?id=jRX6yCxFhx.
53 Solaiman, I. (2023) The Gradient of Generative AI Release: Methods and Considerations. arXiv.
https://arxiv.org/pdf/2302.04844.
54 Framework for Nucleic Acid Synthesis Screening (2024). National Science and Technology Council. OSTP-Nucleic-
Acid_Synthesis_Screening_Framework-Sep2024-Final.pdf (whitehouse.gov).
55 Rein, D. et al., (2023) GPQA: A Graduate-Level Google-Proof Q&A Benchmark. arXiv.
https://arxiv.org/abs/2311.12022; Laurent, J. et al., (2024) LAB-Bench: Measuring Capabilities of Language Models
for Biology Research. arXiv. https://arxiv.org/abs/2407.10362; and Hendrycks, D. et al., (2021) Measuring Massive
Multitask Language Understanding. arXiv. https://arxiv.org/abs/2009.03300.
56 Department of Homeland Security (2024) Reducing the Risks at the Intersection of Artificial Intelligence and
Chemical, Biological, Radiological, and Nuclear Threats Department of Homeland
Security.https://www.dhs.gov/publication/fact-sheet-and-report-dhs-advances-efforts-reduce-risks-intersection-
artificial.
57 The White House (2024) United States Government Policy for Oversight of Dual Use Research of Concern and
Pathogens with Enhanced Pandemic Potential. The White House. https://www.whitehouse.gov/ostp/news-
updates/2024/05/06/united-states-government-policy-for-oversight-of-dual-use-research-of-concern-and-
pathogens-with-enhanced-pandemic-potential/.
58 Rose, S. et al., (2024) The near-term impact of AI on biological
misuse. CLTR.  https://www.longtermresilience.org/reports/the-near-term-impact-of-ai-on-biological-misuse/.
59 Department of Homeland Security (2024) Reducing the Risks at the Intersection of Artificial Intelligence and
Chemical, Biological, Radiological, and Nuclear Threats. Department of Homeland
Security. https://www.dhs.gov/publication/fact-sheet-and-report-dhs-advances-efforts-reduce-risks-intersection-
artificial.
60 Department of Homeland Security (2010) Federal Incident Management Planning. Department of Homeland
Security. https://www.oig.dhs.gov/sites/default/files/assets/Mgmt/OIGr_10-58_Feb10.pdf
61 Biosafety refers to the “practices, controls, and containment infrastructure that reduce the risk of unintentional
exposure to, contamination with, release of, or harm from pathogens, toxins, and biological materials” (NIST
Bioeconomy Lexicon: https://www.nist.gov/bioscience/nist-bioeconomy-lexicon).
62 Biosecurity refers to the “security measures designed to prevent the loss, theft, misuse, diversion, unauthorized
possession or material introduction, or intentional release of pathogens, toxins, biological materials, and related

<!-- page 67 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

62

information and/or technology” (NIST Bioeconomy Lexicon: https://www.nist.gov/bioscience/nist-bioeconomy-
lexicon).
63 Rose, S. et al., (2024) The near-term impact of AI on biological misuse. CLTR.
https://www.longtermresilience.org/reports/the-near-term-impact-of-ai-on-biological-misuse/.
64 Safety considerations for chemical and/or biological AI models. (2024) Federal Register.
https://www.federalregister.gov/documents/2024/10/04/2024-22974/safety-considerations-for-chemical-andor-
biological-ai-models.
65 Building an early warning system for LLM-aided biological threat creation (2024) OpenAI.
https://openai.com/index/building-an-early-warning-system-for-llm-aided-biological-threat-creation/
66 Mouton, C. et al., (2024) The operational risks of AI in large-scale biological attacks: Results of a red-team study.
RAND. https://www.rand.org/pubs/research_reports/RRA2977-2.html.
67 OpenAI o1 System Card (2024). OpenAI. https://cdn.openai.com/o1-system-card-20240917.pdf.
68 Pre-deployment evaluation of Anthropic’s upgraded Claude 3.5 Sonnet. (2024). NIST.
https://www.nist.gov/news-events/news/2024/11/pre-deployment-evaluation-anthropics-upgraded-claude-35-
sonnet.
69 Pre-deployment evaluation of OpenAI’s o1 model (2024). NIST. https://www.nist.gov/news-
events/news/2024/12/pre-deployment-evaluation-openais-o1-model.
70 Useful expert assessment typically draws on diverse expertise including: scientific research, biosecurity, law
enforcement and national security, biodefense, as well as other relevant areas as specified in the USG Policy for
Oversight of Dual Use Research of Concern https://www.whitehouse.gov/ostp/news-updates/2024/05/06/united-
states-government-policy-for-oversight-of-dual-use-research-of-concern-and-pathogens-with-enhanced-
pandemic-potential/.
71 Laurent, J. M., et al., (2024). LAB-Bench: Measuring capabilities of language models for biology research. arXiv.
https://doi.org/10.48550/arXiv.2407.10362.
72 Pre-deployment evaluation of Anthropic’s upgraded Claude 3.5 Sonnet. (2024). NIST.
https://www.nist.gov/news-events/news/2024/11/pre-deployment-evaluation-anthropics-upgraded-claude-35-
sonnet.
73 Pre-deployment evaluation of OpenAI’s o1 model (2024). NIST. https://www.nist.gov/news-
events/news/2024/12/pre-deployment-evaluation-openais-o1-model.
74 Updated responsible scaling policy (2024) Anthropic. https://www.anthropic.com/news/announcing-our-
updated-responsible-scaling-policy.
75 OpenAI’s CBRN tests (2024) Planned Obsolescence. https://www.planned-obsolescence.org/openais-cbrn-tests-
seem-unclear/.
76 Code of Federal Regulations Title 22, Part 121 (2024) U.S. Government Publishing Office.
https://www.ecfr.gov/current/title-22/part-121.
77 The White House (2024) United States Government Policy for Oversight of Dual Use Research of Concern and
Pathogens with Enhanced Pandemic Potential. The White House. https://www.whitehouse.gov/ostp/news-
updates/2024/05/06/united-states-government-policy-for-oversight-of-dual-use-research-of-concern-and-
pathogens-with-enhanced-pandemic-potential/.
78 Carter, S., et al., Developing Guardrails for
AI Biodesign Tools (2024) Nuclear Threat Initiative. https://www.nti.org/analysis/articles/developing-guardrails-
for-ai-biodesign-tools/.
79 Nevo, S., et al. A playbook for securing AI model weights (2024). RAND.
https://www.rand.org/pubs/research_briefs/RBA2849-1.html.
80 Building an early warning system for LLM-aided biological threat creation (2024). OpenAI.
https://openai.com/index/building-an-early-warning-system-for-llm-aided-biological-threat-creation/.
81 The NIST Cybersecurity Framework (CSF) 2.0 (2024). National Institute of Standards and Technology.
https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf; ISO/IEC 27001:2022 (2022). International Standards
Organization. https://www.iso.org/standard/27001.

<!-- page 68 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

63

82 Nation-State Cyber Actors (2024). Cybersecurity and Infrastructure Security Agency.
https://www.cisa.gov/topics/cyber-threats-and-advisories/nation-state-cyber-actors;
How Microsoft names threat actors (2024). Microsoft.  https://learn.microsoft.com/en-us/defender-xdr/microsoft-
threat-actor-naming;
Naming Adversaries and Why It Matters to Your Security Team (2024). CrowdStrike.
https://www.crowdstrike.com/en-us/blog/naming-adversaries-and-why-it-matters-to-security-teams/.
83 Task Force Report: Resilient Military Systems and the Advanced Cyber Threat (2013). Department of Defense
Defense Science Board. https://nsarchive2.gwu.edu/NSAEBB/NSAEBB424/docs/Cyber-081.pdf.
84 Trends on Zero-Days Exploited In-the-Wild in 2023 (2023). Google. https://cloud.google.com/blog/topics/threat-
intelligence/2023-zero-day-trends.
85 Heiding, Fred et. al. Evaluating Large Language Models' Capability to Launch Fully Automated Spear Phishing
Campaigns: Validated on Human Subjects (2024). arXiv. https://arxiv.org/abs/2412.00586 ;  Top Phishing Statistics
for 2025: Latest Figures and Trends (2024). StationX. https://www.stationx.net/phishing-statistics/.
86 The Untold Story of NotPetya, the Most Devastating Cyberattack in History (2018). Wired.
https://www.wired.com/story/notpetya-cyberattack-ukraine-russia-code-crashed-the-world/;
Cyber-attack: US and UK blame North Korea for WannaCry (2017). BBC. https://www.bbc.com/news/world-us-
canada-42407488 .
87 ATT&CK (2024). MITRE. https://attack.mitre.org/.
88 The Cyber Killchain (2024). Lockheed Martin. https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-
kill-chain.html.
89 Cybersecurity Alerts & Advisories (2024). Cybersecurity and Infrastructure Security Agency.
https://www.cisa.gov/news-events/cybersecurity-advisories ; NSA Cybersecurity Advisories and Guidance (2024).
National Security Agency. https://www.nsa.gov/press-room/cybersecurity-advisories-guidance/.
90 Westland, Chris. A Rational Choice Model of Computer and Network Crime (1997). International Journal of
Electronic Commerce.  https://www.jstor.org/stable/27750812.
91 XBOW Validation Benchmarks (2024). XBOW. https://github.com/xbow-engineering/validation-
benchmarks/tree/main.
92 Guide for Conducting Risk Assessments, SP 800 30-r. NIST.
https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-30r1.pdf; An Introduction to the Factor
Analysis of Information Risk (FAIR) (2017). FAIR Institute. https://www.fairinstitute.org/what-is-fair.
93 The Cost of Malicious Cyber Activity to the U.S. Economy (2018). The White House.
https://trumpwhitehouse.archives.gov/wp-content/uploads/2018/02/The-Cost-of-Malicious-Cyber-Activity-to-the-
U.S.-Economy.pdf; Federal Bureau of Investigation Internet Crime Report 2023 (2023). Federal Bureau of
Investigation. https://www.fbi.gov/contact-us/field-offices/sanfrancisco/news/fbi-releases-internet-crime-report ;
Net Losses: Estimating the Global Cost of Cybercrime (2014). Center for Strategic and International Studies.
https://www.csis.org/analysis/net-losses-estimating-global-cost-cybercrime.
94 Anderson, R, Barton, C, Böhme, R, Clayton, R, Gañán, C, Grasso, T, Levi, M, Moore, T & Vasek, M. Measuring the
Changing Cost of Cybercrime (2019). Workshop on the Economics of Information Security.
https://www.researchgate.net/publication/350793602_Measuring_the_changing_cost_of_cybercrime.
95 Sec 15, Information Technology and Cybersecurity Funding, Budget for Fiscal Year 2025 (2024). The White House.
https://www.whitehouse.gov/wp-content/uploads/2024/03/ap_15_it_fy2025.pdf.
96 Chauvin, Timothee. eyeballvul: a future-proof benchmark for vulnerability detection in the wild. arXiv.
https://arxiv.org/abs/2407.08708.
97 AI Cyber Challenge (2024). DARPA. https://aicyberchallenge.com/.
98 Chauvin, Timothee. eyeballvul: a future-proof benchmark for vulnerability detection in the wild.
99 Zhang, Andy, et. al. CyBench: A benchmark for evaluating the cybersecurity capabilities and risks of language
models (2024). arXiv.  https://cybench.github.io/ ; Shao, M. et. al. NYU CTF Dataset: A Scalable Open-Source
Benchmark Dataset for Evaluating LLMs in Offensive Security (2024). arXiv. https://github.com/NYU-LLM-
CTF/NYU_CTF_Bench.

<!-- page 69 -->
NIST AI 800-1 2pd (Second Public Draft)   Managing Misuse Risk for Dual-Use Foundation Models
January 2025, U.S. AI Safety Institute

64

100 Turtayev, Rustem et. al. Hacking CTFs with Plain Agents (2024). arXiv. https://arxiv.org/pdf/2412.02776;
Abramovich, Talor et. al. EnIGMA: Enhanced Interactive Generative Model Agent for CTF Challenges (2024). arXiv.
https://arxiv.org/abs/2409.16165; Waisman, Nico and Dolan-Gavitt, Brendan. How XBOW found a Scoold
authentication bypass (2024). XBOW. https://xbow.com/blog/xbow-scoold-vuln/.
101 Guidelines for capability elicitation (2024). METR. https://metr.github.io/autonomy-evals-guide/elicitation-
protocol/.
102 Glazunov, Sergei and Brand, Mark. Project Naptime: Evaluating Offensive Security Capabilities of Large
Language Models (2024). Google. https://googleprojectzero.blogspot.com/2024/06/project-naptime.html.
103 US AISI and UK AISI Joint Pre-Deployment Test, Anthropic’s Claude 3.5 Sonnet (October 2024 Release) (2024).
US AI Safety Institute and UK AI Safety Institute.
https://www.nist.gov/system/files/documents/2024/11/19/Upgraded%20Sonnet-Publication-US.pdf;  Kapoor,
Sayesh and Narayanan, Arvind. AI leaderboards are no longer useful. It's time to switch to Pareto curves (2024). AI
Snake Oil Blog. https://www.aisnakeoil.com/p/ai-leaderboards-are-no-longer-useful.
104 Evaluations Canary (2024). Alignment Research Center. https://www.alignment.org/canary/.
105 Inspect (2024). UK AI Safety Institute. https://inspect.ai-safety-institute.org.uk/ ; Vivaria (2024). METR.
https://vivaria.metr.org/.
106 Influence and cyber operations: an update (2024). OpenAI. https://cdn.openai.com/threat-intelligence-
reports/influence-and-cyber-operations-an-update_October-2024.pdf.
107 Alexopolous, Nikolaos et. Al. How Long Do Vulnerabilities Live in the Code? A Large-Scale Empirical
Measurement Study on FOSS Vulnerability Lifetimes (2022).
Usenix. https://www.usenix.org/system/files/sec22summer_alexopoulos.pdf.
108 CISA Insights: Remediate Vulnerabilities for Internet-Accessible Systems (2024). Cybersecurity and Infrastructure
Security Agency. https://www.cisa.gov/sites/default/files/publications/CISAInsights-Cyber-
RemediateVulnerabilitiesforInternetAccessibleSystems_S508C.pdf.
109 NIST AI 100-4: Reducing Risks Posed by Synthetic Content (2024). National Institute of Standards and
Technology. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-4.pdf.
110 Lohn, Drew and Jackson, Krystal. Will AI Make Cyber Swords or Shields? (2022) Center for Security and Emerging
Technologies. https://cset.georgetown.edu/publication/will-ai-make-cyber-swords-or-shields/.
111 Kapoor, Sayesh et. al. On the Societal Impact of Open Foundation Models (2024). arXiv.
https://arxiv.org/pdf/2403.07918.
