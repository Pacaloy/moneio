document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#moneyInBtn').onclick = () => console.log('money in');
  document.querySelector('#moneyOutBtn').onclick = () => console.log('money out');

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
  
  document.querySelector('#addAccountBtn').onclick = () => console.log('add account');
  document.querySelector('#addFloatingBtn').onclick = () => console.log('add floating');
}

function loadBreakdown() {

  // View breakdown and hide dashboard
  document.querySelector('#dashboardView').style.display = 'none';
  document.querySelector('#breakdownView').style.display = 'block';
}
