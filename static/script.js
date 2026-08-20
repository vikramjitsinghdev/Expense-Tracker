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
    const budget = Number(budgetElement.value);
    /*
    Frontend validation
    */
    if (!name) {
        showMessage(
            "Please enter your name.",
            "setupMessage"
        );
        return;
    }
    if (isNaN(budget) || budget < 0) {
        showMessage(
            "Please enter a valid budget.",
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
        console.error(error);
        showMessage(
            "Unable to connect to the Flask server.",
            "setupMessage"
        );
    }
}
/*
ADD EXPENSE
*/
async function addExpense() {

    /*
    Get values from HTML.
    */
    const description =document.getElementById("description").value.trim();
    const unitCost = Number(document.getElementById("cost").value);
    const category = document.getElementById("category").value.trim();
    const amount = Number(document.getElementById("amount").value);
    const date = document.getElementById("date").value;
    const payment = document.getElementById("payment").value;
    /*
    Frontend validation.
    */
    if (!description) {
        showMessage(
            "Description cannot be empty.",
            "addMessage"
        );
        return;
    }
    if (isNaN(unitCost) || unitCost <= 0) {
        showMessage(
            "Cost must be greater than 0.",
            "addMessage"
        );
        return;
    }
    if (!category) {
        showMessage(
            "Category cannot be empty.",
            "addMessage"
        );
        return;
    }
    if (isNaN(amount) || amount < 1) {
        showMessage(
            "Quantity must be at least 1.",
            "addMessage"
        );
        return;
    }
    if (!date) {
        showMessage(
            "Please select a date.",
            "addMessage"
        );
        return;
    }
    if (!payment) {
        showMessage(
            "Please select a payment method.",
            "addMessage"
        );
        return;
    }
    /*
    Send the expense to Flask.
    */
    try {
        const response = await fetch("/api/expenses",
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    description: description,
                    unit_cost: unitCost,
                    category: category,
                    amount: amount,
                    date: date,
                    payment: payment
                })
            }
        );
        const data = await response.json();
        /*
        Handle backend errors.
        */
        if (!response.ok) {
            showMessage(
                data.error || "Unable to add expense.",
                "addMessage"
            );
            return;
        }
        /*
        Clear the form.
        */
        clearAddForm();
        /*
        Update dashboard using backend data.
        */
        await updateDashboard();
        /*
        Tell the user the expense was added.
        */
        showMessage(
            "Expense recorded successfully.",
            "addMessage"
        );
    } catch (error) {
        console.error(error);
        showMessage(
            "Unable to connect to the Flask server.",
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
    clearInput("amount");
    clearInput("date");
    const payment = document.getElementById("payment");
    if (payment) { payment.value = "";}
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
            Quantity:${expense.amount}
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
        const response = await fetch(`/api/expenses/${id}`);
        const expense = await response.json();
        if (!response.ok) {
            alert(expense.error ||"Expense not found.");
            return;
        }
        /*
        Put backend data into the edit form.
        */
        document.getElementById("editId").value =expense.id;
        document.getElementById("editDescription").value =expense.description;
        /*
        The backend stores total cost, while the edit form asks for unit cost.
        Therefore: unit cost = total cost / quantity
        */
        document.getElementById("editCost").value =Number(expense.cost / expense.amount).toFixed(2);
        document.getElementById("editCategory").value =expense.category;
        document.getElementById("editAmount").value =expense.amount;
        document.getElementById("editDate").value =expense.date;
        document.getElementById("editPayment").value =expense.payment;
        showScene("editScene");
    } catch (error) {
        console.error(error);
    }
}
/*
SAVE EDIT
*/
async function saveEdit() {
    const id = Number(document.getElementById("editId").value);
    const data = {description:document.getElementById("editDescription").value.trim(),
        unit_cost:Number(document.getElementById("editCost").value),
        category:document.getElementById("editCategory").value.trim(),
        amount:Number(document.getElementById("editAmount").value),
        date:document.getElementById("editDate").value,
        payment:document.getElementById("editPayment").value
    };
    try {
        const response = await fetch(`/api/expenses/${id}`,
                {
                    method: "PUT",headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data)
                }
            );
        const result = await response.json();
        if (!response.ok) {
            alert(result.error || "Unable to update expense.");
            return;
        }
        /*
        Refresh backend information.
        */
        await updateDashboard();
        /*
        Return to expense list.
        */
        await showExpenses();
    } catch (error) {
        console.error(error);
        alert("Unable to connect to the Flask server.");
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
            <td>
                $${Number(expense.cost).toFixed(2)}
            </td>
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