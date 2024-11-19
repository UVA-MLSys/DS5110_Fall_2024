# Testing

Testing the data will be done in `pytest`

1) data integrity
2) model performance
3) system capacity
4) aws connection
5) environments loaded correctly

## Run Tests

From the root directory

```bash
pytest -vvx # run tests
pytest --cov # check test coverage
 	
pytest --cov --cov-report=html:coverage_re # html report if needed
```