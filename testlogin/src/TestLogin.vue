<template>
  <div class="test-login-container">
    <div class="header">
      <h1>Test Login App</h1>
      <Button v-if="session.isLoggedIn" @click="handleLogout" variant="subtle">Logout</Button>
    </div>
    
    <div class="content">
      <div v-if="session.isLoggedIn && userResource.data" class="user-info">
        <div class="info-card">
          <h2>Logged In User Information</h2>
          <div class="user-details">
            <div class="detail-item">
              <strong>Full Name:</strong>
              <span>{{ userResource.data.full_name || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <strong>Email:</strong>
              <span>{{ userResource.data.name || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <strong>User ID:</strong>
              <span>{{ userResource.data.name || 'N/A' }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="loading">
        <p>Loading user information...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Button } from 'frappe-ui'
import { userResource } from '../../shared/data/user'
import { session } from '../../shared/data/session'

const handleLogout = () => {
  session.logout.submit()
}
</script>

<style scoped>
.test-login-container {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0;
  color: #059669;
  font-size: 2rem;
}

.content {
  max-width: 800px;
  margin: 0 auto;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.info-card h2 {
  margin-top: 0;
  color: #059669;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: #f0fdf4;
  border-radius: 8px;
  border-left: 4px solid #10b981;
}

.detail-item strong {
  color: #059669;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-item span {
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 500;
}

.loading {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.loading p {
  color: #6b7280;
  font-size: 1.125rem;
}

@media (max-width: 768px) {
  .test-login-container {
    padding: 1rem;
  }
  
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header h1 {
    font-size: 1.5rem;
    text-align: center;
  }
  
  .info-card {
    padding: 1.5rem;
  }
}
</style>

