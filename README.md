# Hospital Management System using Transaction Chains

## Overview
This project implements a **Hospital Management System** using **Transaction Chains** to optimize concurrency and ensure serializability in a distributed database environment. Inspired by the paper *"Transaction Chains: Achieving Serializability with Low Latency in Geo-Distributed Storage Systems,"* this system models hospital operations as structured transaction chains, allowing efficient execution across distributed nodes.

## Features
- **Transaction Chains for Serializability:** Transactions are divided into hops executed sequentially across distributed nodes.
- **Efficient Data Partitioning:** Data is partitioned based on geographic location for optimized retrieval and storage.
- **Low-Latency Transactions:** The system allows partial execution before finalizing transactions, reducing response times.
- **Scalability:** Designed to handle high concurrent loads and large-scale healthcare operations.
- **Security & Atomicity:** Ensures per-hop isolation, all-or-nothing atomicity, and origin ordering for robust transaction processing.

## System Design
### **Architecture**
The system follows a **hybrid distributed architecture**, consisting of **7 database nodes** that communicate asynchronously using WebSockets. Each node manages a subset of hospital data and executes specific transaction hops.

### **Database Schema**
The system uses multiple distributed databases with the following key tables:
- **Patients (s1, s6):** Stores patient records.
- **Doctors (s2):** Maintains doctor details.
- **Appointments (s3):** Tracks patient-doctor appointments.
- **Medical Records (s4):** Stores patient diagnoses and treatments.
- **Prescriptions (s5):** Manages patient prescriptions.
- **Billing (s7):** Handles hospital invoices.

### **Partition Strategy**
- **Patients Table:** Partitioned by geographic region for efficient lookup.
- **Appointments & Doctors:** Stored on separate nodes for optimized scheduling.
- **Medical Records & Billing:** Ensures security and privacy by keeping them on dedicated nodes.

## Transactions
Transactions are executed as structured chains:
- **T1: Booking an Appointment**
  - Hop 1: Read Patients Table
  - Hop 2: Read Doctors Table
  - Hop 3: Insert into Appointments Table
- **T2: Inserting Medical Records**
  - Hop 1: Read Patients Table
  - Hop 2: Insert into Medical Records
  - Hop 3: Insert into Prescriptions
- **T3: Billing Process**
  - Hop 1: Read Patients Table
  - Hop 2: Insert into Billing Table
  - Hop 3: Update Appointments Table
- **T4: Follow-up Appointment**
  - Hop 1: Read Patients Table
  - Hop 2: Read Medical Records
  - Hop 3: Read Doctors Table
  - Hop 4: Insert into Appointments Table

## SC Graph & Conflict Analysis
The system constructs **Serialization Conflict (SC) Graphs** to analyze dependencies and detect cycles, ensuring conflict-free execution. Key properties include:
- **Per-hop isolation:** Ensures each hop executes independently.
- **All-or-nothing atomicity:** If one hop fails, the entire chain is rolled back.
- **Origin ordering:** Transactions starting on the same node retain order across nodes.

## Performance Evaluation
- Tested under **10 to 200 concurrent transactions**.
- **Average execution time remains stable** despite increasing transaction load.
- **Throughput decreases** with higher concurrency due to increased contention.
- Future optimizations include **dynamic transaction handling and SC cycle elimination** for enhanced concurrency.

## Future Improvements
- Implement **dynamic chain splitting** for higher concurrency.
- Extend to support **larger datasets and geographically dispersed nodes**.
- Improve **query optimization** for faster transaction execution.


## References
- "Transaction Chains: Achieving Serializability with Low Latency in Geo-Distributed Storage Systems"
- Related works on **distributed databases, sagas, and transaction chopping**.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/sumitraut7/CS223-Transaction-Chains.git
   cd CS223-Transaction-Chains
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## License
This project is licensed under the MIT License.

