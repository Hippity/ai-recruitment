import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Grid,
  Alert,
  Snackbar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogContentText,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
} from '@mui/material';
import { Add as AddIcon, FilterList as FilterIcon } from '@mui/icons-material';
import { useJobs } from '../hooks/useJobs';
import { useEntities } from '../hooks/useEntities';
import JobCard from '../components/jobs/JobCard';
import JobForm from '../components/jobs/JobForm';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { JOB_STATUSES, JOB_STATUS_LABELS } from '../utils/constants';

const JobsPage = ({ selectedEntityId, onNavigateToCriteria }) => {
  const { entities } = useEntities();
  const { 
    jobs, 
    loading, 
    error, 
    createJob, 
    updateJob, 
    deleteJob,
    fetchJobs 
  } = useJobs(selectedEntityId);

  const [formOpen, setFormOpen] = useState(false);
  const [editingJob, setEditingJob] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingJob, setDeletingJob] = useState(null);
  const [formLoading, setFormLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  // Filters
  const [filters, setFilters] = useState({
    entityId: selectedEntityId || '',
    status: '',
    search: '',
  });

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const handleCreateJob = () => {
    setEditingJob(null);
    setFormOpen(true);
  };

  const handleEditJob = (job) => {
    setEditingJob(job);
    setFormOpen(true);
  };

  const handleDeleteJob = (job) => {
    setDeletingJob(job);
    setDeleteDialogOpen(true);
  };

  const handleViewCriteria = (job) => {
    onNavigateToCriteria(job.id);
  };

  const handleViewDetails = (job) => {
    // TODO: Implement job details view
    console.log('View job details:', job);
  };

  const handleFormSubmit = async (formData) => {
    setFormLoading(true);
    try {
      if (editingJob) {
        await updateJob(editingJob.id, formData);
        showSnackbar('Job updated successfully');
      } else {
        await createJob(formData);
        showSnackbar('Job created successfully');
      }
      setFormOpen(false);
      setEditingJob(null);
    } catch (error) {
      showSnackbar(error.message || 'Operation failed', 'error');
    } finally {
      setFormLoading(false);
    }
  };

  const confirmDelete = async () => {
    try {
      await deleteJob(deletingJob.id);
      showSnackbar('Job deleted successfully');
      setDeleteDialogOpen(false);
      setDeletingJob(null);
    } catch (error) {
      showSnackbar(error.message || 'Failed to delete job', 'error');
    }
  };

  const handleFilterChange = (field, value) => {
    const newFilters = { ...filters, [field]: value };
    setFilters(newFilters);
    
    // Apply filters
    fetchJobs({
      entityId: newFilters.entityId || null,
      status: newFilters.status || null,
    });
  };

  const filteredJobs = jobs.filter(job => {
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      return (
        job.title.toLowerCase().includes(searchLower) ||
        job.reference_number.toLowerCase().includes(searchLower) ||
        job.description.toLowerCase().includes(searchLower)
      );
    }
    return true;
  });

  const getEntityName = (entityId) => {
    const entity = entities.find(e => e.id === entityId);
    return entity ? entity.name : 'Unknown Entity';
  };

  if (loading && jobs.length === 0) {
    return <LoadingSpinner message="Loading jobs..." />;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3} width={"80vw"}>
        <Typography variant="h4" component="h1">
          Jobs
          {selectedEntityId && (
            <Typography variant="subtitle1" color="text.secondary">
              for {getEntityName(selectedEntityId)}
            </Typography>
          )}
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreateJob}
        >
          Create Job
        </Button>
      </Box>

      {/* Filters */}
      <Box mb={3} sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Entity</InputLabel>
          <Select
            value={filters.entityId}
            onChange={(e) => handleFilterChange('entityId', e.target.value)}
            label="Entity"
          >
            <MenuItem value="">All Entities</MenuItem>
            {entities.map((entity) => (
              <MenuItem key={entity.id} value={entity.id}>
                {entity.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
            label="Status"
          >
            <MenuItem value="">All Statuses</MenuItem>
            {Object.values(JOB_STATUSES).map((status) => (
              <MenuItem key={status} value={status}>
                {JOB_STATUS_LABELS[status]}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          size="small"
          placeholder="Search jobs..."
          value={filters.search}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          sx={{ minWidth: 200 }}
        />
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {filteredJobs.length === 0 ? (
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          minHeight="300px"
          textAlign="center"
        >
          <Typography variant="h6" color="text.secondary" gutterBottom>
            {jobs.length === 0 ? 'No jobs found' : 'No jobs match your filters'}
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={2}>
            {jobs.length === 0 
              ? 'Create your first job to get started'
              : 'Try adjusting your search criteria'
            }
          </Typography>
          {jobs.length === 0 && (
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleCreateJob}
            >
              Create Job
            </Button>
          )}
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredJobs.map((job) => (
            <Grid item xs={12} sm={6} md={4} key={job.id}>
              <JobCard
                job={job}
                onEdit={handleEditJob}
                onDelete={handleDeleteJob}
                onViewCriteria={handleViewCriteria}
                onViewDetails={handleViewDetails}
              />
            </Grid>
          ))}
        </Grid>
      )}

      <JobForm
        open={formOpen}
        onClose={() => {
          setFormOpen(false);
          setEditingJob(null);
        }}
        onSubmit={handleFormSubmit}
        job={editingJob}
        loading={formLoading}
        entities={entities}
      />

      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Delete Job</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete "{deletingJob?.title}"? 
            This action cannot be undone and will also delete all associated criteria.
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

export default JobsPage;