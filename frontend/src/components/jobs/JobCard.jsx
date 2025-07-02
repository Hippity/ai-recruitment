import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Chip,
  Box,
} from '@mui/material';
import {
  MoreVert as MoreVertIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Assignment as AssignmentIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';
import { JOB_STATUS_LABELS, JOB_STATUS_COLORS } from '../../utils/constants';

const JobCard = ({ job, onEdit, onDelete, onViewCriteria, onViewDetails }) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleEdit = () => {
    onEdit(job);
    handleMenuClose();
  };

  const handleDelete = () => {
    onDelete(job);
    handleMenuClose();
  };

  const handleViewCriteria = () => {
    onViewCriteria(job);
    handleMenuClose();
  };

  const handleViewDetails = () => {
    onViewDetails(job);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const totalCriteria = (job.min_qualification_criteria_count || 0) + 
                       (job.formal_assessment_criteria_count || 0);

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', width: 300 }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
          <Typography variant="h6" component="h2" gutterBottom>
            {job.title}
          </Typography>
          <IconButton
            size="small"
            onClick={handleMenuClick}
            aria-label="more actions"
          >
            <MoreVertIcon />
          </IconButton>
        </Box>

        <Typography variant="body2" color="text.secondary" gutterBottom>
          Ref: {job.reference_number}
        </Typography>

        <Typography 
          variant="body2" 
          color="text.secondary" 
          paragraph
          sx={{
            display: '-webkit-box',
            WebkitLineClamp: 3,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
            minHeight: '60px',
          }}
        >
          {job.description}
        </Typography>

        <Box display="flex" flexDirection="column" gap={1} mb={2}>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Chip
              label={JOB_STATUS_LABELS[job.status]}
              size="small"
              color={JOB_STATUS_COLORS[job.status]}
              variant="outlined"
            />
            {job.cutoff_grade && (
              <Chip
                label={`Cutoff: ${job.cutoff_grade}`}
                size="small"
                variant="outlined"
              />
            )}
          </Box>

          <Box display="flex" alignItems="center" gap={1}>
            <AssignmentIcon fontSize="small" color="action" />
            <Typography variant="caption">
              {totalCriteria} Criteria
              {totalCriteria > 0 && (
                <> ({job.min_qualification_criteria_count || 0} Min Qual, {job.formal_assessment_criteria_count || 0} Formal)</>
              )}
            </Typography>
          </Box>
        </Box>

        <Typography variant="caption" color="text.secondary">
          Created: {formatDate(job.created_at)}
        </Typography>
      </CardContent>

      <CardActions>
        <Button size="small" onClick={handleViewCriteria} startIcon={<AssignmentIcon />}>
          Criteria
        </Button>
      </CardActions>

      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleMenuClose}
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        <MenuItem onClick={handleEdit}>
          <EditIcon fontSize="small" sx={{ mr: 1 }} />
          Edit
        </MenuItem>
        <MenuItem onClick={handleDelete} sx={{ color: 'error.main' }}>
          <DeleteIcon fontSize="small" sx={{ mr: 1 }} />
          Delete
        </MenuItem>
      </Menu>
    </Card>
  );
};

export default JobCard;