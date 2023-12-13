document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#moneyInBtn').onclick = () => loadMoneio(true);
  document.querySelector('#moneyOutBtn').onclick = () => loadMoneio(false);
  document.querySelector('#transferMoneyBtn').onclick = loadAddTransfer;

  // Use buttons to toggle between views
  document.querySelector('#dashboardBtn').onclick = loadDashboard;
  document.querySelector('#breakdownBtn').onclick = loadBreakdown;
  document.querySelector('#transfersBtn').onclick = loadTransfers;

  switch(sessionStorage.getItem('display')) {
    case 'dashboard':
      loadDashboard();
      break;
    case 'transactions':
      loadBreakdown();
      break;
    case 'transfers':
      loadTransfers();
      break;
    default:
      loadDashboard();
  }
});

function loadDashboard() {
  sessionStorage.setItem('display', 'dashboard');

  // View dashboard and hide breakdown and transfers
  document.querySelector('#defaultView').style.display = 'block';
  document.querySelector('#dashboardView').style.display = 'block';
  document.querySelector('#breakdownView').style.display = 'none';
  document.querySelector('#transfersView').style.display = 'none';
  document.querySelector('#addAccountView').style.display = 'none';
  document.querySelector('#moneioView').style.display = 'none';
  document.querySelector('#addTransferView').style.display = 'none';

  document.querySelector('#addAccountBtn').onclick = () => loadAddAccount(false);
  document.querySelector('#addFloatingBtn').onclick = () => loadAddAccount(true);
  document.querySelector('#addDeductiblesBtn').onclick = () => loadAddAccount(true, true);
}

function loadBreakdown() {
  sessionStorage.setItem('display', 'transactions');

  // View breakdown and hide dashboard and transfers
  document.querySelector('#dashboardView').style.display = 'none';
  document.querySelector('#breakdownView').style.display = 'block';
  document.querySelector('#transfersView').style.display = 'none';
  document.querySelector('#addAccountView').style.display = 'none';
  document.querySelector('#moneioView').style.display = 'none';
  document.querySelector('#addTransferView').style.display = 'none';
}

function loadTransfers() {
  sessionStorage.setItem('display', 'transfers');

  // View transfers and hide dashboard and breakdown
  document.querySelector('#dashboardView').style.display = 'none';
  document.querySelector('#breakdownView').style.display = 'none';
  document.querySelector('#transfersView').style.display = 'block';
  document.querySelector('#addAccountView').style.display = 'none';
  document.querySelector('#moneioView').style.display = 'none';
  document.querySelector('#addTransferView').style.display = 'none';
}

function loadAddAccount(isFloating = false, isDeductibles = false) {

  // View add account view and hide default view
  document.querySelector('#defaultView').style.display = 'none';
  document.querySelector('#addAccountView').style.display = 'block';

  // Close button to return to default view
  document.querySelector('#cancelAddAccountViewBtn').onclick = () => {
    document.querySelector('#defaultView').style.display = 'block';
    document.querySelector('#addAccountView').style.display = 'none';
  };

  // Assign default date today
  document.querySelector('#formAccountDate').value = getFormattedDateToday();

  // Confirm button to add account
  document.querySelector('#form-account').onsubmit = () => {
    
    // Add account
    fetch('/account', {
      method: 'POST',
      body: JSON.stringify({
        name: document.querySelector('#formAccountName').value,
        balance: `${isDeductibles ? '-' : ''}${document.querySelector('#formAccountInitialBalance').value}`,
        date: document.querySelector('#formAccountDate').value,
        isFloating: isFloating,
      }),
    })
    .then(() => {
      setTimeout(() => {
        window.location.reload();
      }, 300)
    });

    return false;
  };
}

function loadMoneio(isMoneyIn) {
  
  // Money label
  if (isMoneyIn) {
    document.querySelector('#moneioMoneyLabel').innerHTML = 'Money In:';
  } else {
    document.querySelector('#moneioMoneyLabel').innerHTML = 'Money Out:';
  }

  // View moneio view and hide default view
  document.querySelector('#defaultView').style.display = 'none';
  document.querySelector('#moneioView').style.display = 'block';

  // Close button to return to default view 
  document.querySelector('#cancelMoneioViewBtn').onclick = () => {
    document.querySelector('#defaultView').style.display = 'block';
    document.querySelector('#moneioView').style.display = 'none';
  };

  // Go to dashboard to create new account
  if (document.querySelector('#createAccountBtn')) document.querySelector('#createAccountBtn').onclick = loadDashboard;

  // Assign default date today
  document.querySelector('#formMoneioDate').value = getFormattedDateToday();

  // Confirm to add/minus money to an account
  document.querySelector('#form-moneio').onsubmit = () => {

    // Add money in/money out
    fetch('/moneio', {
      method: 'POST',
      body: JSON.stringify({
        name: document.querySelector('#formMoneioName').value,
        money: document.querySelector('#formMoneioMoney').value,
        account: document.querySelector('#formMoneioAccount').value,
        date: document.querySelector('#formMoneioDate').value,
        isMoneyIn: isMoneyIn,
      }),
    })
    .then(() => {
      setTimeout(() => {
        window.location.reload();
      }, 300)
    });

    return false;
  };
}

function loadAddTransfer() {

  // View transfer and hide default view
  document.querySelector('#defaultView').style.display = 'none';
  document.querySelector('#addTransferView').style.display = 'block';

  // Close button to return to default view
  document.querySelector('#cancelAddTransferViewBtn').onclick = () => {
    document.querySelector('#defaultView').style.display = 'block';
    document.querySelector('#addTransferView').style.display = 'none';
  };

  // Go to dashboard to create new account
  if (document.querySelector('#createAccountBtn2')) document.querySelector('#createAccountBtn2').onclick = loadDashboard;

  // Assign default date today
  document.querySelector('#formTransferDate').value = getFormattedDateToday();

  // Confirm to add new transfer
  document.querySelector('#form-transfer').onsubmit = () => {

    // Add money in/money out
    fetch('/transfer', {
      method: 'POST',
      body: JSON.stringify({
        name: document.querySelector('#formTransferName').value,
        price: document.querySelector('#formTransferAmount').value,
        fromAccount: document.querySelector('#formFromAccount').value,
        toAccount: document.querySelector('#formToAccount').value,
        date: document.querySelector('#formTransferDate').value,
      }),
    })
    .then(() => {
      setTimeout(() => {
        window.location.reload();
      }, 300)
    });

    return false;
  };
}

function getFormattedDateToday() {
  const today = new Date();
  const yyyy = today.getFullYear();
  let mm = today.getMonth() + 1; // Months start at 0!
  let dd = today.getDate();
  
  if (dd < 10) dd = '0' + dd;
  if (mm < 10) mm = '0' + mm;

  return yyyy + '-' + mm + '-' + dd;
}
