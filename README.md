
# TOPSIS Assignment  
Name: Rohan Malhotra  
Roll Number: 102303437  

---

## Introduction

This project implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method as part of the given assignment.  
The objective of TOPSIS is to rank a set of alternatives based on their relative closeness to the ideal best and ideal worst solutions.

The complete assignment is implemented in three parts:
1. Command-line TOPSIS program in Python  
2. Python package created and uploaded to PyPI  
3. Web-based TOPSIS service that emails the result file to the user  

All assignment rules, validations, and constraints have been strictly followed.

---

## Part I – Command Line TOPSIS Program

### Description

This part implements TOPSIS as a **Python command-line application**.  
The program accepts an input CSV file, a list of weights, and a list of impacts, and produces an output CSV file containing the **Topsis Score** and **Rank** for each alternative.

---

### Command Format


python topsis.py <inputFileName> <weights> <impacts> <outputFileName>


---

### Example Command

```bash
python topsis.py data.csv "1,1,1,1,1" "+,+,-,+,+" output-result.csv
```

---

### Input Specifications

* The input file must be a **CSV file**
* The file must contain **at least three columns**
* The **first column** represents the alternatives
* The **second column to the last column** must contain **numeric values only**
* Weights must be:

  * Numeric
  * Comma-separated
* Impacts must be:

  * Comma-separated
  * Either `+` (benefit) or `-` (cost)

---

### Output Specifications

* The output file is generated in **CSV format**
* The output file contains:

  * All original columns
  * A new column **Topsis Score**
  * A new column **Rank**
* Rank 1 represents the **best alternative**

---

### Validations Implemented

The following validations are implemented as per assignment guidelines:

* Correct number of command-line arguments
* Input file existence check (File Not Found handling)
* Minimum of three columns in input file
* Numeric validation for all criteria columns
* Equal number of weights, impacts, and criteria columns
* Impacts restricted to only `+` or `-`
* Proper comma-separated format for weights and impacts
* Meaningful error messages for invalid inputs

---

## Part II – Python Package (PyPI)

The command-line TOPSIS program from Part I is converted into a **reusable Python package** and uploaded to **PyPI**.

---

### Package Name

```text
Topsis-RohanMalhotra-102303437
```

---

### Installation

```bash
pip install Topsis-RohanMalhotra-102303437
```

---

### Usage After Installation

```bash
topsis <inputFileName> <weights> <impacts> <outputFileName>
```

---

### Example Usage

```bash
topsis data.csv "1,1,1,1,1" "+,+,-,+,+" output.csv
```

---

### PyPI Link

PASTE YOUR PYPI LINK HERE
Example:
[[https://pypi.org/project/Topsis-RohanMalhotra-102303437/](https://pypi.org/project/Topsis-RohanMalhotra-102303437/)](https://pypi.org/project/Topsis-RohanMalhotra-102303437/1.0.0/)

---

### Notes

* The PyPI package provides the same functionality and validations as the command-line program
* The executable command `topsis` becomes available after installation
* Output format and ranking logic remain unchanged

---

## Part III – Web-Based TOPSIS Application

A web-based TOPSIS application is developed to provide a graphical interface for users.

---

### Features

* Upload input file in **CSV or XLSX** format
* Enter weights and impacts through the web form
* Enter recipient email address
* Perform all validations as in CLI and PyPI versions
* Send the result CSV file to the user via email

---

### Web Application Link

PASTE YOUR HOSTED WEBSITE LINK HERE (Render URL)
Example:
[[https://topsis-rohan.onrender.com](https://topsis-rohan.onrender.com)](https://topsis-rohanmalhotra--RohanMalhotra7.replit.app)

---

### Email Functionality

* The user enters the **recipient email address** in the frontend
* SMTP credentials are configured securely using environment variables
* The result CSV file is sent as an **email attachment**
* No email credentials are exposed in the frontend or source code

---

## Security Considerations

* Email credentials are not hardcoded
* Sensitive information is stored as environment variables on the hosting platform
* Only the recipient email is taken as user input
* The application follows secure deployment practices

---

## Project Structure

```text
.
├── part1/
│   └── topsis.py
├── package_template/
│   ├── pyproject.toml
│   └── src/
│       └── topsis_rohanmalhotra_102303437/
├── web/
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
└── README.md
```

---

## Assumptions

* The first column of the input file contains alternative names
* Criteria values are numeric
* Internet connectivity is available for email delivery
* SMTP service is properly configured on the hosting platform

---

## Conclusion

This project successfully fulfills all requirements of the TOPSIS assignment by implementing:

* A validated command-line TOPSIS program
* A reusable Python package published on PyPI
* A web-based TOPSIS application with email-based result delivery

All parts have been implemented strictly according to the assignment guidelines.

```
```
