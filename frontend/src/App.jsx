import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import Layout from './components/common/Layout';
import EntitiesPage from './pages/EntitiesPage';
import JobsPage from './pages/JobsPage';
import CriteriaPage from './pages/CriteriaPage';

// Create a custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          '&:hover': {
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
});

function App() {
  const [currentPage, setCurrentPage] = useState('entities');
  const [selectedEntityId, setSelectedEntityId] = useState(null);
  const [selectedJobId, setSelectedJobId] = useState(null);

  const handleNavigate = (page, id = null) => {
    setCurrentPage(page);
    
    if (page === 'jobs' && id) {
      setSelectedEntityId(id);
      setSelectedJobId(null);
    } else if (page === 'criteria' && id) {
      setSelectedJobId(id);
    } else if (page === 'entities') {
      setSelectedEntityId(null);
      setSelectedJobId(null);
    }
  };

  const handleNavigateToJobs = (entityId) => {
    handleNavigate('jobs', entityId);
  };

  const handleNavigateToCriteria = (jobId) => {
    handleNavigate('criteria', jobId);
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'entities':
        return <EntitiesPage onNavigateToJobs={handleNavigateToJobs} />;
      case 'jobs':
        return (
          <JobsPage 
            selectedEntityId={selectedEntityId} 
            onNavigateToCriteria={handleNavigateToCriteria}
          />
        );
      case 'criteria':
        return <CriteriaPage selectedJobId={selectedJobId} />;
      default:
        return <EntitiesPage onNavigateToJobs={handleNavigateToJobs} />;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Layout 
        currentPage={currentPage} 
        onNavigate={handleNavigate}
      >
        {renderCurrentPage()}
      </Layout>
    </ThemeProvider>
  );
}

export default App;