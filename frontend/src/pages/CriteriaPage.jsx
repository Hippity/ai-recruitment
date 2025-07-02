import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Alert,
  Snackbar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogContentText,
  Paper,
  Tabs,
  Tab,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { 
  Add as AddIcon,
  CheckCircle as CheckCircleIcon,
  Assignment as AssignmentIcon,
} from '@mui/icons-material';
import { useCriteria } from '../hooks/useCriteria';
import { useJobs } from '../hooks/useJobs';
import MinQualificationForm from '../components/criteria/MinQualificationForm';
import FormalAssessmentForm from '../components/criteria/FormalAssessmentForm';
import CriteriaList from '../components/criteria/CriteriaList';
import LoadingSpinner from '../components/common/LoadingSpinner';

const CriteriaPage = ({ selectedJobId }) => {
  const { jobs } = useJobs();
  const {
    criteria,
    loading,
    error,
    createMinQualificationCriteria,
    updateMinQualificationCriteria,
    deleteMinQualificationCriteria,
    createFormalAssessmentCriteria,
    updateFormalAssessmentCriteria,
    deleteFormalAssessmentCriteria,
  } = useCriteria(selectedJobId);

  const [currentJobId, setCurrentJobId] = useState(selectedJobId || '');
  const [tabValue, setTabValue] = useState(0);
  const [minQualFormOpen, setMinQualFormOpen] = useState(false);
  const [formalFormOpen, setFormalFormOpen] = useState(false);
  const [editingCriteria, setEditingCriteria] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingCriteria, setDeletingCriteria] = useState(null);
  const [formLoading, setFormLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const handleJobChange = (jobId) => {
    setCurrentJobId(jobId);
    // The useCriteria hook will automatically refetch when jobId changes
  };

  const getJobInfo = () => {
    return jobs.find(job => job.id === parseInt(currentJobId));
  };

  // Minimum Qualification Handlers
  const handleAddMinQual = () => {
    setEditingCriteria(null);
    setMinQualFormOpen(true);
  };

  const handleEditMinQual = (criteria) => {
    setEditingCriteria(criteria);
    setMinQualFormOpen(true);
  };

  const handleDeleteMinQual = (criteria) => {
    setDeletingCriteria({ ...criteria, type: 'min_qual' });
    setDeleteDialogOpen(true);
  };

  const handleMinQualSubmit = async (formData) => {
    setFormLoading(true);
    try {
      if (editingCriteria) {
        await updateMinQualificationCriteria(editingCriteria.id, formData);
        showSnackbar('Minimum qualification criteria updated successfully');
      } else {
        await createMinQualificationCriteria(formData);
        showSnackbar('Minimum qualification criteria added successfully');
      }
      setMinQualFormOpen(false);
      setEditingCriteria(null);
    } catch (error) {
      showSnackbar(error.message || 'Operation failed', 'error');
    } finally {
      setFormLoading(false);
    }
  };

  // Formal Assessment Handlers
  const handleAddFormal = () => {
    setEditingCriteria(null);
    setFormalFormOpen(true);
  };

  const handleEditFormal = (criteria) => {
    setEditingCriteria(criteria);
    setFormalFormOpen(true);
  };

  const handleDeleteFormal = (criteria) => {
    setDeletingCriteria({ ...criteria, type: 'formal' });
    setDeleteDialogOpen(true);
  };

  const handleFormalSubmit = async (formData) => {
    setFormLoading(true);
    try {
      if (editingCriteria) {
        await updateFormalAssessmentCriteria(editingCriteria.id, formData);
        showSnackbar('Formal assessment criteria updated successfully');
      } else {
        await createFormalAssessmentCriteria(formData);
        showSnackbar('Formal assessment criteria added successfully');
      }
      setFormalFormOpen(false);
      setEditingCriteria(null);
    } catch (error) {
      showSnackbar(error.message || 'Operation failed', 'error');
    } finally {
      setFormLoading(false);
    }
  };

  const confirmDelete = async () => {
    try {
      if (deletingCriteria.type === 'min_qual') {
        await deleteMinQualificationCriteria(deletingCriteria.id);
        showSnackbar('Minimum qualification criteria deleted successfully');
      } else {
        await deleteFormalAssessmentCriteria(deletingCriteria.id);
        showSnackbar('Formal assessment criteria deleted successfully');
      }
      setDeleteDialogOpen(false);
      setDeletingCriteria(null);
    } catch (error) {
      showSnackbar(error.message || 'Failed to delete criteria', 'error');
    }
  };

  if (!currentJobId) {
    return (
      <Box>
        <Typography variant="h4" component="h1" gutterBottom>
          Job Criteria
        </Typography>
        
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Select a Job
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={3}>
            Choose a job to manage its assessment criteria
          </Typography>
          
          <FormControl sx={{ minWidth: 300 }}>
            <InputLabel>Select Job</InputLabel>
            <Select
              value=""
              onChange={(e) => handleJobChange(e.target.value)}
              label="Select Job"
            >
              {jobs.map((job) => (
                <MenuItem key={job.id} value={job.id}>
                  {job.title} ({job.reference_number})
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Paper>
      </Box>
    );
  }

  if (loading) {
    return <LoadingSpinner message="Loading criteria..." />;
  }

  const jobInfo = getJobInfo();

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3} width={"80vw"}>
        <div>
          <Typography variant="h4" component="h1">
            Job Criteria
          </Typography>
          {jobInfo && (
            <Typography variant="subtitle1" color="text.secondary">
              {jobInfo.title} ({jobInfo.reference_number})
            </Typography>
          )}
        </div>
        
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Job</InputLabel>
          <Select
            value={currentJobId}
            onChange={(e) => handleJobChange(e.target.value)}
            label="Job"
          >
            {jobs.map((job) => (
              <MenuItem key={job.id} value={job.id}>
                {job.title}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ mb: 3 }}>
        <Tabs 
          value={tabValue} 
          onChange={(e, newValue) => setTabValue(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab 
            label={
              <Box display="flex" alignItems="center" gap={1}>
                <CheckCircleIcon fontSize="small" />
                Minimum Qualification
                <Box 
                  component="span" 
                  sx={{ 
                    ml: 1, 
                    px: 1, 
                    py: 0.25, 
                    backgroundColor: 'primary.main', 
                    color: 'white', 
                    borderRadius: 1, 
                    fontSize: '0.75rem' 
                  }}
                >
                  {criteria.min_qualification_criteria.length}
                </Box>
              </Box>
            } 
          />
          <Tab 
            label={
              <Box display="flex" alignItems="center" gap={1}>
                <AssignmentIcon fontSize="small" />
                Formal Assessment
                <Box 
                  component="span" 
                  sx={{ 
                    ml: 1, 
                    px: 1, 
                    py: 0.25, 
                    backgroundColor: 'primary.main', 
                    color: 'white', 
                    borderRadius: 1, 
                    fontSize: '0.75rem' 
                  }}
                >
                  {criteria.formal_assessment_criteria.length}
                </Box>
              </Box>
            } 
          />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {tabValue === 0 && (
            <Box>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                <Typography variant="h6">
                  Minimum Qualification Criteria
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={handleAddMinQual}
                >
                  Add Criteria
                </Button>
              </Box>
              
              <CriteriaList
                criteria={criteria.min_qualification_criteria}
                type="min_qual"
                onEdit={handleEditMinQual}
                onDelete={handleDeleteMinQual}
                title=""
                emptyMessage="No minimum qualification criteria added yet. These are pass/fail requirements that candidates must meet."
              />
            </Box>
          )}

          {tabValue === 1 && (
            <Box>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                <Typography variant="h6">
                  Formal Assessment Criteria
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={handleAddFormal}
                >
                  Add Criteria
                </Button>
              </Box>
              
              <CriteriaList
                criteria={criteria.formal_assessment_criteria}
                type="formal"
                onEdit={handleEditFormal}
                onDelete={handleDeleteFormal}
                title=""
                emptyMessage="No formal assessment criteria added yet. These are scored evaluations that contribute to the candidate's final grade."
              />
            </Box>
          )}
        </Box>
      </Paper>

      {/* Forms */}
      <MinQualificationForm
        open={minQualFormOpen}
        onClose={() => {
          setMinQualFormOpen(false);
          setEditingCriteria(null);
        }}
        onSubmit={handleMinQualSubmit}
        criteria={editingCriteria}
        loading={formLoading}
      />

      <FormalAssessmentForm
        open={formalFormOpen}
        onClose={() => {
          setFormalFormOpen(false);
          setEditingCriteria(null);
        }}
        onSubmit={handleFormalSubmit}
        criteria={editingCriteria}
        loading={formLoading}
      />

      {/* Delete Confirmation */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Delete Criteria</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this criteria for "{deletingCriteria?.area}"? 
            This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={confirmDelete} color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert 
          onClose={handleCloseSnackbar} 
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default CriteriaPage;