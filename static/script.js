/*
GLOBAL FRONTEND STATE
*/
// Stores the current user's name for displaying it in the UI.
let userName = "";
/*
UTILITY FUNCTIONS
*/
// Display a message inside an element.
function showMessage(message, elementId = "message") {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
    }
}
// Clear an input field.
function clearInput(id) {
    const element = document.getElementById(id);
    if (element) {
        element.value = "";
    }
}
/*
START TRACKER
*/
async function startTracker() {
    const nameElement = document.getElementById("name");
    const budgetElement = document.getElementById("budget");
    const name = nameElement.value.trim();
    const budgetText = budgetElement.value.trim();
    if (!name) {
        showMessage("Please enter your name.",
            "setupMessage"
        );
        return;
    }
    if (!/^\d+(\.\d{1,2})?$/.test(budgetText)) {
        showMessage(
            "Budget must be a valid number with up to 2 decimal places.",
            "setupMessage"
        );
        return;
    }
    const budget = Number(budgetText);
    if (
        !Number.isFinite(budget) ||
        budget <= 0 ||
        budget > 1000000000
    ) {
        showMessage(
            "Budget must be greater than 0 and no more than $1,000,000,000.",
            "setupMessage"
        );
        return;
    }
    /*
    Send the user's information to the Flask backend.
    */
    try {
        const response = await fetch("/api/start",
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    name: name,
                    budget: budget
                })
            }
        );
        const data = await response.json();
        /*
        Check whether Flask returned an error.
        */
        if (!response.ok) {
            showMessage(
                data.error || "Unable to start tracker.",
                "setupMessage"
            );
            return;
        }
        /*
        Save the name only for displaying
        it in the frontend.
        */
        userName = data.name;
        /*
        Update the welcome message.
        */
        const userDisplay = document.getElementById("userDisplay");
        if (userDisplay) {
            userDisplay.textContent = `Welcome, ${userName}`;
        }
        /*
        Move to the dashboard.
        */
        showScene("dashboardScene");
        /*
        Get the latest budget information
        from Flask.
        */
        await updateDashboard();
    } catch (error) {
        console.error(
            "START TRACKER ERROR:",
            error
        );
        showMessage(
            `Error: ${error.message}`,
            "setupMessage"
        );
    }
}
/*
ADD EXPENSE
*/
async function addExpense() {

    // --------------------------------------------------------
    // Get HTML elements
    // --------------------------------------------------------
    const descriptionElement = document.getElementById("description");
    const costElement = document.getElementById("cost");
    const categoryElement = document.getElementById("category");
    const quantityElement = document.getElementById("quantity");
    const dateElement = document.getElementById("date");
    const paymentElement = document.getElementById("payment");
    // -------------------------------------------------------
    // Make sure all elements exist
    // --------------------------------------------------------
    if (
        !descriptionElement ||
        !costElement ||
        !categoryElement ||
        !quantityElement ||
        !dateElement ||
        !paymentElement
    ) {
        console.error(
            "One or more expense form elements are missing."
        );
        showMessage(
            "There is a problem with the expense form.",
            "addMessage"
        );
        return;
    }
    // --------------------------------------------------------
    // Get raw values
    // --------------------------------------------------------
    const description = descriptionElement.value.trim();
    const costText = costElement.value.trim();
    const category = categoryElement.value.trim();
    const quantityText = quantityElement.value.trim();
    const date = dateElement.value;
    const payment = paymentElement.value;
    // --------------------------------------------------------
    // DESCRIPTION
    // --------------------------------------------------------
    if (!description) {
        showMessage(
            "Description cannot be empty.",
            "addMessage"
        );
        return;
    }
    // --------------------------------------------------------
    // COST
    // --------------------------------------------------------
    if (
        !/^\d+(\.\d{1,2})?$/.test(costText)
    ) {
        showMessage(
            "Cost must be a valid number with up to 2 decimal places.",
            "addMessage"
        );
        return;
    }
    const unitCost =
        Number(costText);
    if (
        !Number.isFinite(unitCost) ||
        unitCost <= 0 ||
        unitCost > 1000000
    ) {
        showMessage(
            "Cost must be greater than 0 and no more than $1,000,000.",
            "addMessage"
        );
        return;
    }
    // --------------------------------------------------------
    // CATEGORY
    // --------------------------------------------------------
    if (
        !/^[A-Za-z]+(?: [A-Za-z]+)*$/.test(category)
    ) {
        showMessage(
            "Category must contain letters and spaces only.",
            "addMessage"
        );
        return;
    }
    // --------------------------------------------------------
    // QUANTITY
    // --------------------------------------------------------
    if (!/^\d+$/.test(quantityText)) {

        showMessage(
            "Quantity must be a whole number.",
            "addMessage"
        );
        return;
    }
    const quantity =
        Number(quantityText);
    if (
        !Number.isSafeInteger(quantity) ||
        quantity < 1 ||
        quantity > 100000
    ) {
        showMessage(
            "Quantity must be between 1 and 100000.",
            "addMessage"
        );
        return;
    }
    // --------------------------------------------------------
    // DATE
    // --------------------------------------------------------
    if (!date) {
        showMessage(
            "Please select a date.",
            "addMessage"
        );
        return;
    }
    // --------------------------------------------------------
    // PAYMENT
    // --------------------------------------------------------
    if (!payment) {
        showMessage(
            "Please select a payment method.",
            "addMessage"
        );
        return;
    }
    // --------------------------------------------------------
    // SEND DATA TO FLASK
    // --------------------------------------------------------
    try {
        const response = await fetch(
            "/api/expenses",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    description: description,
                    unit_cost: unitCost,
                    category: category,
                    amount: quantity,
                    date: date,
                    payment: payment
                })
            }
        );
        const data =
            await response.json();
        // ----------------------------------------------------
        // Backend rejected request
        // ----------------------------------------------------
        if (!response.ok) {
            showMessage(
                data.error ||
                "Unable to add expense.",
                "addMessage"
            );
            return;
        }
        // ----------------------------------------------------
        // Successfully added
        // ----------------------------------------------------
        clearAddForm();
        await updateDashboard();
        showMessage(
            "Expense recorded successfully.",
            "addMessage"
        );
    } catch (error) {
        console.error(
            "ADD EXPENSE ERROR:",
            error
        );
        showMessage(
            `Error: ${error.message}`,
            "addMessage"
        );
    }
}
/*
CLEAR ADD EXPENSE FORM
*/
function clearAddForm() {
    clearInput("description");
    clearInput("cost");
    clearInput("category");
    clearInput("quantity");
    clearInput("date");
    const payment =document.getElementById("payment");
    if (payment) {payment.value = "";}
    const message = document.getElementById("addMessage");
    if (message) {message.textContent = "";}
}
/*
GET ALL EXPENSES
*/
async function getExpenses() {
    try {
        const response = await fetch("/api/expenses");
        const data = await response.json();
        if (!response.ok) {
            console.error( data.error ||"Unable to retrieve expenses.");
            return [];
        }
        return data;
    } catch (error) {
        console.error(error);
        return [];
    }
}
/*
DISPLAY ALL EXPENSES
*/
async function showExpenses() {
    const expenses = await getExpenses();
    const table = document.getElementById("expenseTable");
    if (!table) {
        return;
    }
    table.innerHTML = "";
    /*
    If there are no expenses.
    */
    if (expenses.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="8">
                    No expenses recorded.
                </td>
            </tr>
        `;
        showScene("expensesScene");
        return;
    }
    /*
    Create one table row for each expense returned by Flask.
    */
    expenses.forEach(expense => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${expense.id}</td>
            <td>${expense.description}</td>
            <td>${expense.category}</td>
            <td>${expense.amount}</td>
            <td>$${Number(expense.cost).toFixed(2)}</td>
            <td>${expense.date}</td>
            <td>${expense.payment}</td>
            <td class="actions">
                <button
                    onclick="editExpense(${expense.id})">
                    Edit
                </button>
                <button
                    class="danger"
                    onclick="deleteExpense(${expense.id})">
                    Delete
                </button>
            </td>
        `;
        table.appendChild(row);
    });
    showScene("expensesScene");
}
/*
SEARCH BY ID
*/
async function searchById() {
    const id = Number(document.getElementById("searchId").value);
    if (!id) {
        showMessage(
            "Please enter an expense number.",
            "searchResults"
        );
        return;
    }
    try {
        const response = await fetch(`/api/expenses/${id}`);
        const data = await response.json();
        if (!response.ok) {document.getElementById("searchResults").innerHTML = `
                <p class="message">
                    ${data.error}
                </p>
            `;
            return;
        }
        displaySearchResult(data);
    } catch (error) {
        console.error(error);
    }
}
/*
SEARCH BY DATE
*/
async function searchByDate() {
    const date = document.getElementById("searchDate").value;
    if (!date) {
        showMessage(
            "Please select a date.",
            "searchResults"
        );
        return;
    }
    try {
        const response = await fetch(`/api/expenses/date/${date}`);
        const results = await response.json();
        if (!response.ok) {document.getElementById("searchResults").innerHTML = `
                <p class="message">
                    ${results.error}
                </p>
            `;
            return;
        }
        if (results.length === 0) {document.getElementById("searchResults").innerHTML = `
                <p class="message">
                    No expenses found for this date.
                </p>
            `;
            return;
        }
        document.getElementById("searchResults").innerHTML = results.map(
            expense => `
                <div class="message">
                    <strong>
                        Expense #${expense.id}
                    </strong>
                    <br>
                    ${expense.description}
                    <br>
                    $${Number(expense.cost).toFixed(2)}|${expense.category}|${expense.payment}
                </div>
            `
        ).join("");
    } catch (error) {
        console.error(error);
    }
}
/*
DISPLAY SEARCH RESULT
*/
function displaySearchResult(expense) {document.getElementById("searchResults").innerHTML = `
        <div class="message">
            <strong>
                Expense #${expense.id}
            </strong>
            <br>
            Description:${expense.description}
            <br>
            Category:${expense.category}
            <br>
            Quantity:${expense.quantity}
            <br>
            Cost:$${Number(expense.cost).toFixed(2)}
            <br>
            Date:${expense.date}
            <br>
            Payment:${expense.payment}
        </div>
    `;
}
/*
EDIT EXPENSE
*/
async function editExpense(id) {
    try {
        const response =await fetch(`/api/expenses/${id}`);
        const expense =await response.json();
        if (!response.ok) {
            alert(expense.error ||"Expense not found.");
            return;
        }
        document.getElementById("editId").value = expense.id;
        document.getElementById("editDescription").value = expense.description;
        document.getElementById("editCost").value =Number(expense.unit_cost).toFixed(2);
        document.getElementById("editCategory").value = expense.category;
        document.getElementById("editAmount").value = expense.amount;
        document.getElementById("editDate").value = expense.date;
        document.getElementById("editPayment").value = expense.payment;
        showScene("editScene");
    } catch (error) {
        console.error("EDIT EXPENSE ERROR:",
            error
        );
        alert(`Error: ${error.message}`);
    }
}
/*
SAVE EDIT
*/
async function saveEdit() {
    const id = Number( document.getElementById("editId").value);
    const data = {
        description:
            document.getElementById("editDescription").value.trim(),
        unit_cost:
            document.getElementById("editCost").value.trim(),
        category:
            document.getElementById("editCategory").value.trim(),
        amount:
            document.getElementById("editAmount").value.trim(),
        date:
            document.getElementById("editDate").value,
        payment:
            document.getElementById("editPayment").value
    };
    try {
        const response =
            await fetch(`/api/expenses/${id}`,
                {
                    method: "PUT",
                    headers: {"Content-Type":"application/json"
                    },
                    body: JSON.stringify(data)
                }
            );
        const result =await response.json();
        if (!response.ok) {
            alert(result.error ||"Unable to update expense.");
            return;
        }
        await updateDashboard();
        await showExpenses();
    } catch (error) {
        console.error("SAVE EDIT ERROR:",
            error
        );
        alert(`Error: ${error.message}`);
    }
}
/*
DELETE EXPENSE
*/
async function deleteExpense(id) {
    const confirmed = confirm("Are you sure you want to delete this expense?");
    if (!confirmed) {
        return;
    }
    try {
        const response = await fetch(`/api/expenses/${id}`,
                {
                    method: "DELETE"
                }
            );
        const data = await response.json();
        if (!response.ok) { 
            alert(data.error || "Unable to delete expense.");
            return;
        }
        /*
        Refresh dashboard.
        */
        await updateDashboard();
        /*
        Refresh expense table.
        */
        await showExpenses();
    } catch (error) {
        console.error(error);
        alert("Unable to connect to the Flask server.");
    }
}
/*
SORT BY DATE
*/
async function sortExpensesByDate() {
    try {
        const response = await fetch("/api/expenses/sort/date");
        const expenses = await response.json();
        if (!response.ok) {
            return;
        }
        displayExpenses(expenses);
    } catch (error) {console.error(error)}
}
/*
SORT BY ID
*/
async function sortExpensesById() {
    try {
        const response = await fetch("/api/expenses/sort/id");
        const expenses = await response.json();
        if (!response.ok) {
            return;
        }
        displayExpenses(expenses);
    } catch (error) {
        console.error(error);
    }
}
/*
DISPLAY EXPENSES
*/
function displayExpenses(expenses) {
    const table = document.getElementById("expenseTable");
    if (!table) {
        return;
    }
    table.innerHTML = "";
    if (expenses.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="8">
                    No expenses recorded.
                </td>
            </tr>
        `;
        showScene("expensesScene");
        return;
    }
    expenses.forEach(expense => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${expense.id}</td>
            <td>${expense.description}</td>
            <td>${expense.category}</td>
            <td>${expense.amount}</td>
            <td>$${Number(expense.cost).toFixed(2)}</td>
            <td>${expense.date}</td>
            <td>${expense.payment}</td>
            <td class="actions">
                <button
                    onclick="editExpense(${expense.id})">
                    Edit
                </button>
                <button
                    class="danger"
                    onclick="deleteExpense(${expense.id})">
                    Delete
                </button>
            </td>
        `;
        table.appendChild(row);
    });
    showScene("expensesScene");
}
/*
UPDATE DASHBOARD
*/
async function updateDashboard() {
    try {
        const response = await fetch("/api/budget");
        const data = await response.json();
        if (!response.ok) {
            return;
        }
        const budgetDisplay = document.getElementById("budgetDisplay");
        const spentDisplay = document.getElementById("spentDisplay");
        const remainingDisplay = document.getElementById("remainingDisplay");
        if (budgetDisplay) {
            budgetDisplay.textContent =`$${Number(data.total_budget).toFixed(2)}`;
        }
        if (spentDisplay) {
            spentDisplay.textContent = `$${Number(data.total_spent).toFixed(2)}`;
        }
        if (remainingDisplay) {
            remainingDisplay.textContent = `$${Number(data.remaining_budget).toFixed(2)}`;
        }
    } catch (error) {
        console.error(error);
    }
}
/*
SCENE MANAGEMENT
*/
function showScene(sceneId) {
    const scenes = document.querySelectorAll(".scene");
    scenes.forEach(scene => {
        scene.classList.remove("active");});
    const target = document.getElementById(sceneId);
    if (target) {
        target.classList.add("active");
    }
}
function cancelExpense() {
    clearAddForm();
    showScene("dashboardScene");
}
/*
DISPLAY ITEMS
*/
async function showItems() {
    try {
        const response = await fetch("/api/items");

        const items = await response.json();

        const table = document.getElementById("itemsTable");
        if (!table) {
            return;
        }
        table.innerHTML = "";
        if (!response.ok) {
            table.innerHTML = `
                <tr>
                    <td colspan="4">
                        ${items.error ||
                        "Unable to retrieve items."}
                    </td>
                </tr>
            `;
            showScene("itemsScene");
            return;
        }
        if (items.length === 0) {
            table.innerHTML = `
                <tr>
                    <td colspan="4">
                        No items recorded.
                    </td>
                </tr>
            `;
            showScene("itemsScene");
            return;
        }
        items.forEach(item => {
            const row =
                document.createElement("tr");
            row.innerHTML = `
                <td>${item.item}</td>
                <td>
                    $${Number(
                        item.unit_cost
                    ).toFixed(2)}
                </td>
                <td>${item.date}</td>
                <td>${item.quantity}</td>
            `;
            table.appendChild(row);
        });
        showScene("itemsScene");
    } catch (error) {
        console.error(error);
        showMessage(
            "Unable to connect to the Flask server.",
            "message"
        );
    }
}