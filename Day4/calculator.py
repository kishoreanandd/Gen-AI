from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
   return {"message": "Simple Calculator API"}


@app.get("/add")
def add(num1: float, num2: float):
    return {"result": num1 + num2}


@app.get("/subtract")
def subtract(num1: float, num2: float):
    return {"result": num1 - num2}


@app.get("/multiply")
def multiply(num1: float, num2: float):
    return {"result": num1 * num2}


@app.get("/divide")
def divide(num1: float, num2: float):
    if num2 == 0:
        return {"error": "Cannot divide by zero"}

    return {"result": num1 / num2}