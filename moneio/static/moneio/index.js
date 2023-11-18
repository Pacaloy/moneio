document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#moneyInBtn').onclick = loadMoneio;
  document.querySelector('#moneyOutBtn').onclick = loadMoneio;

  // Use buttons to toggle between views
  document.querySelector('#dashboardBtn').onclick = loadDashboard;
  document.querySelector('#breakdownBtn').onclick = loadBreakdown;

  // By default, load the dashboard
  loadDashboard();
});

function loadDashboard() {

  // View dashboard and hide breakdown
  document.querySelector('#dashboardView').style.display = 'block';
  document.querySelector('#breakdownView').style.display = 'none';
  document.querySelector('#addAccountView').style.display = 'none';
  document.querySelector('#moneioView').style.display = 'none';

  document.querySelector('#addAccountBtn').onclick = () => loadAddAccount(false);
  document.querySelector('#addFloatingBtn').onclick = () => loadAddAccount(true);
}

function loadBreakdown() {

  // View breakdown and hide dashboard
  document.querySelector('#dashboardView').style.display = 'none';
  document.querySelector('#breakdownView').style.display = 'block';
}

function loadAddAccount(isFloating) {

  // View add account view and hide default view
  document.querySelector('#defaultView').style.display = 'none';
  document.querySelector('#addAccountView').style.display = 'block';

  // Close button to return to default view
  document.querySelector('#cancelAddAccountViewBtn').onclick = () => {
    document.querySelector('#defaultView').style.display = 'block';
    document.querySelector('#addAccountView').style.display = 'none';
  };

  // Confirm button to add account
  document.querySelector('#form-account').onsubmit = () => {
    
    // Add account
    fetch('/account', {
      method: 'POST',
      body: JSON.stringify({
        name: document.querySelector('#formAccountName').value,
        balance: document.querySelector('#formAccountInitialBalance').value,
        date: document.querySelector('#formAccountDate').value,
        isFloating: isFloating,
      }),
    })
    .then(() => window.location.reload());

    return false;
  };
}

function loadMoneio() {
  
  // View moneio view and hide default view
  document.querySelector('#defaultView').style.display = 'none';
  document.querySelector('#moneioView').style.display = 'block';

  // Close button to return to default view 
  document.querySelector('#cancelMoneioViewBtn').onclick = () => {
    document.querySelector('#defaultView').style.display = 'block';
    document.querySelector('#moneioView').style.display = 'none';
  };
}
