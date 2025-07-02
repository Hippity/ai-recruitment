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
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useEntities } from '../hooks/useEntities';
import EntityCard from '../components/entities/EntityCard';
import EntityForm from '../components/entities/EntityForm';
import LoadingSpinner from '../components/common/LoadingSpinner';

const EntitiesPage = ({ onNavigateToJobs }) => {
  const { 
    entities, 
    loading, 
    error, 
    createEntity, 
    updateEntity, 
    deleteEntity 
  } = useEntities();

  const [formOpen, setFormOpen] = useState(false);
  const [editingEntity, setEditingEntity] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingEntity, setDeletingEntity] = useState(null);
  const [formLoading, setFormLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const handleCreateEntity = () => {
    setEditingEntity(null);
    setFormOpen(true);
  };

  const handleEditEntity = (entity) => {
    setEditingEntity(entity);
    setFormOpen(true);
  };

  const handleDeleteEntity = (entity) => {
    setDeletingEntity(entity);
    setDeleteDialogOpen(true);
  };

  const handleViewJobs = (entity) => {
    onNavigateToJobs(entity.id);
  };

  const handleFormSubmit = async (formData) => {
    setFormLoading(true);
    try {
      if (editingEntity) {
        await updateEntity(editingEntity.id, formData);
        showSnackbar('Entity updated successfully');
      } else {
        await createEntity(formData);
        showSnackbar('Entity created successfully');
      }
      setFormOpen(false);
      setEditingEntity(null);
    } catch (error) {
      showSnackbar(error.message || 'Operation failed', 'error');
    } finally {
      setFormLoading(false);
    }
  };

  const confirmDelete = async () => {
    try {
      await deleteEntity(deletingEntity.id);
      showSnackbar('Entity deleted successfully');
      setDeleteDialogOpen(false);
      setDeletingEntity(null);
    } catch (error) {
      showSnackbar(error.message || 'Failed to delete entity', 'error');
    }
  };

  if (loading && entities.length === 0) {
    return <LoadingSpinner message="Loading entities..." />;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3} width={"80vw"}>
        <Typography variant="h4" component="h1">
          Entities
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreateEntity}
        >
          Create Entity
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {entities.length === 0 ? (
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          minHeight="300px"
          textAlign="center"
        >
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No entities found
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={2}>
            Create your first entity to get started
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateEntity}
          >
            Create Entity
          </Button>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {entities.map((entity) => (
            <Grid item xs={12} sm={6} md={4} key={entity.id}>
              <EntityCard
                entity={entity}
                onEdit={handleEditEntity}
                onDelete={handleDeleteEntity}
                onViewJobs={handleViewJobs}
              />
            </Grid>
          ))}
        </Grid>
      )}

      <EntityForm
        open={formOpen}
        onClose={() => {
          setFormOpen(false);
          setEditingEntity(null);
        }}
        onSubmit={handleFormSubmit}
        entity={editingEntity}
        loading={formLoading}
      />

      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Delete Entity</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete "{deletingEntity?.name}"? 
            This action cannot be undone.
            {deletingEntity?.jobs_count > 0 && (
              <Alert severity="warning" sx={{ mt: 2 }}>
                This entity has {deletingEntity.jobs_count} associated jobs. 
                You cannot delete an entity with jobs.
              </Alert>
            )}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>
            Cancel
          </Button>
          <Button 
            onClick={confirmDelete} 
            color="error"
            disabled={deletingEntity?.jobs_count > 0}
          >
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

export default EntitiesPage;