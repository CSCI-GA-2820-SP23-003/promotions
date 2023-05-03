# NYU DevOps Project - Promotion

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-SP23-003/promotions/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-003/promotions/actions)
[![Build Status](https://github.com/CSCI-GA-2820-SP23-003/promotions/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-003/promotions/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP23-003/promotions/branch/master/graph/badge.svg?token=KS7TVGHDHQ)](https://codecov.io/gh/CSCI-GA-2820-SP23-003/promotions)


This service is currently hosted on a Kubernetes Cluster on IBM Cloud.

Development Site : http://159.122.187.73:31001/  
Production  Site : http://159.122.187.73:31002/

## Project Overview

This repo is the promotion functionality which is part of a demo e-commerce website. It allows for creation of multiple promotion for products. The service supports all CRUD: create, read, update, delete, list and query operations on the main schemas of promotions.

We support 3 types of promotions:
| Promo Type         | Description
| ------------------ | -------------------------------
| BOGO | Buy 1, Get 1.
| DISCOUNT   | Reduce $amount % from your total.
| FIXED | Deduct fix amount from your total

These are the API endpoints of `promotions`

| Index              | Endpoint
| ------------------ | -------------------------------
| Create a Promotion | POST `/promotions` 
| Update an existing Promo | PUT `/promotions/<promotion_id>`
| Activate an existing Promo | PUT `/promotions/<promotion_id>/activate`
| Delete an Promo | DELETE `/promotions/<promotion_id>`
| Deactivate an existing Promo | DELETE `/promotions/<promotion_id>/activate`
| List all Promos     | GET `/promotions`
| Read/Get an Promo by ID   | GET `/promotions/<promotion_id>`


## Project Setup

This project use docker container, VScode. To deploy locally, you can clone this repo, change into the repo directory then use "code ." to start the remote container in VScode ( remote connection extension is required)
```
$ git clone https://github.com/CSCI-GA-2820-SP23-003/promotions.git
$ cd promotions
$ code .
```

To start the service, this project uses honcho which gets it's commands from the Procfile. You can use `honcho start` then open the service in your browser via `localhost:8000`
```
$ honcho start
```

The test cases can be run with `nosetests`
```
$ nosettests
```


## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.


