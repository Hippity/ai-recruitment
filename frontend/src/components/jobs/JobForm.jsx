import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography,
} from '@mui/material';
import { JOB_STATUSES, JOB_STATUS_LABELS } from '../../utils/constants';

const JobForm = ({ 
  open, 
  onClose, 
  onSubmit, 
  job = null, 
  loading = false, 
  entities = [] 
}) => {
  const [formData, setFormData] = useState({
    entity_id: job?.entity_id || '',
    reference_number: job?.reference_number || '',
    title: job?.title || '',
    description: job?.description || '',
    cutoff_grade: job?.cutoff_grade || '',
    status: job?.status || JOB_STATUSES.DRAFT,
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (job) {
      setFormData({
        entity_id: job.entity_id || '',
        reference_number: job.reference_number || '',
        title: job.title || '',
        description: job.description || '',
        cutoff_grade: job.cutoff_grade || '',
        status: job.status || JOB_STATUSES.DRAFT,
      });
    } else {
      setFormData({
        entity_id: '',
        reference_number: '',
        title: '',
        description: '',
        cutoff_grade: '',
        status: JOB_STATUSES.DRAFT,
      });
    }
    setErrors({});
  }, [job, open]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.entity_id) {
      newErrors.entity_id = 'Entity is required';
    }
    
    if (!formData.reference_number.trim()) {
      newErrors.reference_number = 'Reference number is required';
    }
    
    if (!formData.title.trim()) {
      newErrors.title = 'Job title is required';
    }
    
    if (!formData.description.trim()) {
      newErrors.description = 'Job description is required';
    }
    
    if (formData.cutoff_grade && (isNaN(formData.cutoff_grade) || formData.cutoff_grade < 0 || formData.cutoff_grade > 100)) {
      newErrors.cutoff_grade = 'Cutoff grade must be a number between 0 and 100';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const submitData = {
      ...formData,
      cutoff_grade: formData.cutoff_grade ? parseFloat(formData.cutoff_grade) : null,
    };

    onSubmit(submitData);
  };

  const handleClose = () => {
    setErrors({});
    onClose();
  };

  return (
    <Dialog 
      open={open} 
      onClose={handleClose} 
      maxWidth="md" 
      fullWidth
      PaperProps={{
        component: 'form',
        onSubmit: handleSubmit,
      }}
    >
      <DialogTitle>
        {job ? 'Edit Job' : 'Create New Job'}
      </DialogTitle>
      
      <DialogContent>
        <Box sx={{ pt: 1 }}>
          <FormControl 
            fullWidth 
            margin="normal" 
            error={!!errors.entity_id}
            disabled={loading || !!job}
          >
            <InputLabel>Entity</InputLabel>
            <Select
              name="entity_id"
              value={formData.entity_id}
              onChange={handleChange}
              label="Entity"
            >
              {entities.map((entity) => (
                <MenuItem key={entity.id} value={entity.id}>
                  {entity.name}
                </MenuItem>
              ))}
            </Select>
            {errors.entity_id && (
              <Typography variant="caption" color="error" sx={{ mt: 0.5, ml: 2 }}>
                {errors.entity_id}
              </Typography>
            )}
          </FormControl>

          <TextField
            margin="normal"
            name="reference_number"
            label="Reference Number"
            type="text"
            fullWidth
            variant="outlined"
            value={formData.reference_number}
            onChange={handleChange}
            error={!!errors.reference_number}
            helperText={errors.reference_number}
            required
            disabled={loading}
          />
          
          <TextField
            margin="normal"
            name="title"
            label="Job Title"
            type="text"
            fullWidth
            variant="outlined"
            value={formData.title}
            onChange={handleChange}
            error={!!errors.title}
            helperText={errors.title}
            required
            disabled={loading}
          />
          
          <TextField
            margin="normal"
            name="description"
            label="Job Description"
            fullWidth
            variant="outlined"
            multiline
            rows={6}
            value={formData.description}
            onChange={handleChange}
            error={!!errors.description}
            helperText={errors.description}
            required
            disabled={loading}
          />

          <TextField
            margin="normal"
            name="cutoff_grade"
            label="Cutoff Grade"
            type="number"
            fullWidth
            variant="outlined"
            value={formData.cutoff_grade}
            onChange={handleChange}
            error={!!errors.cutoff_grade}
            helperText={errors.cutoff_grade || 'Optional - minimum grade required to pass'}
            inputProps={{ min: 0, max: 100, step: 0.01 }}
            disabled={loading}
          />

          <FormControl fullWidth margin="normal" disabled={loading}>
            <InputLabel>Status</InputLabel>
            <Select
              name="status"
              value={formData.status}
              onChange={handleChange}
              label="Status"
            >
              {Object.values(JOB_STATUSES).map((status) => (
                <MenuItem key={status} value={status}>
                  {JOB_STATUS_LABELS[status]}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </DialogContent>
      
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>
          Cancel
        </Button>
        <Button 
          type="submit" 
          variant="contained" 
          disabled={loading}
        >
          {job ? 'Update' : 'Create'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default JobForm;