import React, { useState } from 'react';
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
import { CRITERIA_AREAS } from '../../utils/constants';

const MinQualificationForm = ({ 
  open, 
  onClose, 
  onSubmit, 
  criteria = null, 
  loading = false 
}) => {
  const [formData, setFormData] = useState({
    area: criteria?.area || '',
    criteria: criteria?.criteria || '',
    explanation: criteria?.explanation || '',
    order_index: criteria?.order_index || 1,
  });
  const [errors, setErrors] = useState({});

  React.useEffect(() => {
    if (criteria) {
      setFormData({
        area: criteria.area || '',
        criteria: criteria.criteria || '',
        explanation: criteria.explanation || '',
        order_index: criteria.order_index || 1,
      });
    } else {
      setFormData({
        area: '',
        criteria: '',
        explanation: '',
        order_index: 1,
      });
    }
    setErrors({});
  }, [criteria, open]);

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
    
    if (!formData.area.trim()) {
      newErrors.area = 'Area is required';
    }
    
    if (!formData.criteria.trim()) {
      newErrors.criteria = 'Criteria is required';
    }
    
    if (formData.order_index && (isNaN(formData.order_index) || formData.order_index < 1)) {
      newErrors.order_index = 'Order index must be a positive number';
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
      order_index: parseInt(formData.order_index) || 1,
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
        {criteria ? 'Edit Minimum Qualification Criteria' : 'Add Minimum Qualification Criteria'}
      </DialogTitle>
      
      <DialogContent>
        <Box sx={{ pt: 1 }}>
          <FormControl 
            fullWidth 
            margin="normal" 
            error={!!errors.area}
            disabled={loading}
          >
            <InputLabel>Area</InputLabel>
            <Select
              name="area"
              value={formData.area}
              onChange={handleChange}
              label="Area"
            >
              {CRITERIA_AREAS.map((area) => (
                <MenuItem key={area} value={area}>
                  {area}
                </MenuItem>
              ))}
            </Select>
            {errors.area && (
              <Typography variant="caption" color="error" sx={{ mt: 0.5, ml: 2 }}>
                {errors.area}
              </Typography>
            )}
          </FormControl>
          
          <TextField
            margin="normal"
            name="criteria"
            label="Criteria"
            fullWidth
            variant="outlined"
            multiline
            rows={4}
            value={formData.criteria}
            onChange={handleChange}
            error={!!errors.criteria}
            helperText={errors.criteria || 'Describe the minimum qualification requirement'}
            required
            disabled={loading}
          />
          
          <TextField
            margin="normal"
            name="explanation"
            label="Additional Explanation"
            fullWidth
            variant="outlined"
            multiline
            rows={3}
            value={formData.explanation}
            onChange={handleChange}
            helperText="Optional - provide additional context or examples"
            disabled={loading}
          />

          <TextField
            margin="normal"
            name="order_index"
            label="Display Order"
            type="number"
            fullWidth
            variant="outlined"
            value={formData.order_index}
            onChange={handleChange}
            error={!!errors.order_index}
            helperText={errors.order_index || 'Order in which this criteria appears (1, 2, 3, ...)'}
            inputProps={{ min: 1, step: 1 }}
            disabled={loading}
          />
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
          {criteria ? 'Update' : 'Add'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default MinQualificationForm;