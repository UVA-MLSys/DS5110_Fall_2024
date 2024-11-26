# Testing

Testing the data will be done in `pytest`

1) data integrity
2) model performance (`integration test`)
3) system capacity
4) aws connection
5) environments loaded correctly

## Run Tests

From the root directory

```bash
make tests # preferred

# if issue with make 
pytest -vvx # run tests
pytest --cov # check test coverage
 	
pytest --cov --cov-report=html:coverage_re # html report if needed
```