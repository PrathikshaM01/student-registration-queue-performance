# Student Registration Queue Performance Modeling

## 1. Project Overview

This project focuses on analyzing the performance of a **student registration queue system** using real registration transaction data. The system consists of **500 student registration records** and **four registration officers**.

The purpose of the project is to investigate how effectively the registration system handles student arrivals and service requests and to identify potential performance bottlenecks.

The system is modeled as a **multi-server queuing system (M/M/4)**, where students represent arriving customers and the four registration officers represent parallel service servers.

## 2. Problem Statement

During student registration periods, multiple students may arrive within a limited period. When the number of arriving students exceeds the available service capacity, students may experience increased waiting times and queue congestion.

This project evaluates whether the four registration officers can efficiently handle the workload represented by the 500 student records. The analysis focuses on waiting time, service time, throughput, queue behavior, and officer utilization.

## 3. Dataset

The dataset contains **500 student registration transactions**.

Each record contains information related to the student's registration process, including:

* Student ID
* Officer ID
* Arrival Time
* Service Start Time
* Service End Time
* Service Time
* Waiting Time
* Time in System

The four registration officers are identified as:

* O_01
* O_02
* O_03
* O_04

The dataset is used to calculate performance measures and evaluate the behavior of the registration queue.

## 4. Performance Objectives

The main objectives of the project are:

1. **Minimize Student Waiting Time**
   Analyze the time students spend waiting before registration service begins.

2. **Evaluate Officer Utilization**
   Determine how effectively the four registration officers are being utilized and compare their workloads.

3. **Evaluate Throughput**
   Examine how efficiently the system processes the 500 student registrations.

4. **Identify Bottlenecks**
   Identify areas where congestion, long waiting times, or high resource utilization may reduce system performance.

5. **Evaluate Resource Allocation**
   Determine whether the current four-officer configuration provides sufficient capacity for the observed workload.

6. **Assess Overall System Performance**
   Use queuing analysis and performance measures to evaluate the efficiency and effectiveness of the registration system.

## 5. Modeling Approach

The student registration process is represented using an **M/M/4 queuing model**.

* **M** – Student arrivals are treated as a stochastic arrival process.
* **M** – Registration service times are treated as a stochastic service process.
* **4** – Four registration officers are available to provide service.

The model is used to evaluate the relationship between student arrival rates, service capacity, queue behavior, and officer utilization.

## 6. Expected Outcomes

The project is expected to provide an understanding of:

* Student waiting-time patterns
* Registration service efficiency
* Officer workload and utilization
* Queue congestion
* System throughput
* Potential bottlenecks
* Appropriate registration capacity

The findings can be used to support decisions about staffing and resource allocation within the student registration process.

## 7. Project Scope

This repository contains the initial problem definition, dataset, and performance objectives for the student registration performance modeling project. Further analysis, calculations, visualizations, and modeling results will be developed as part of the subsequent stages of the project.
