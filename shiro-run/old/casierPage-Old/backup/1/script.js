function incrementValue(pizzaId) {
    var inputElement = document.getElementById("counterInput" + pizzaId);
    var currentValue = parseInt(inputElement.value);
    inputElement.value = currentValue + 1;
    calculateTotalPrice();
  }
  
  function decrementValue(pizzaId) {
    var inputElement = document.getElementById("counterInput" + pizzaId);
    var currentValue = parseInt(inputElement.value);
    if (currentValue > 0) {
      inputElement.value = currentValue - 1;
      calculateTotalPrice();
    }
  }
  
  function calculateTotalPrice() {
    var pizza1Count = parseInt(document.getElementById("counterInput1").value);
    var pizza2Count = parseInt(document.getElementById("counterInput2").value);
    var totalPrice = (pizza1Count * 10) + (pizza2Count * 12); // Assuming pizza 1 costs $10 and pizza 2 costs $12
    document.getElementById("totalPrice").textContent = "$" + totalPrice;
  }
  
  function submitPizza() {
    var pizza1Count = parseInt(document.getElementById("counterInput1").value);
    var pizza2Count = parseInt(document.getElementById("counterInput2").value);
    var totalPrice = (pizza1Count * 10) + (pizza2Count * 12); // Assuming pizza 1 costs $10 and pizza 2 costs $12
    alert("You have selected " + pizza1Count + " Pizza 1 and " + pizza2Count + " Pizza 2. Total price: $" + totalPrice);
  }
  