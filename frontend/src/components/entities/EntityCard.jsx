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
  Work as WorkIcon,
} from '@mui/icons-material';

const EntityCard = ({ entity, onEdit, onDelete, onViewJobs }) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleEdit = () => {
    onEdit(entity);
    handleMenuClose();
  };

  const handleDelete = () => {
    onDelete(entity);
    handleMenuClose();
  };

  const handleViewJobs = () => {
    onViewJobs(entity);
    handleMenuClose();
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' , width: 200 }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Typography variant="h6" component="h2" gutterBottom>
            {entity.name}
          </Typography>
          <IconButton
            size="small"
            onClick={handleMenuClick}
            aria-label="more actions"
          >
            <MoreVertIcon />
          </IconButton>
        </Box>

        <Typography 
          variant="body2" 
          color="text.secondary" 
          paragraph
          sx={{
            display: '-webkit-box',
            WebkitLineClamp: 3,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}
        >
          {entity.description || 'No description provided'}
        </Typography>

        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <WorkIcon fontSize="small" color="action" />
          <Chip
            label={`${entity.jobs_count || 0} Jobs`}
            size="small"
            variant="outlined"
          />
        </Box>

        <Typography variant="caption" color="text.secondary">
          Created: {formatDate(entity.created_at)}
        </Typography>
      </CardContent>

      <CardActions>
        <Button size="small" onClick={handleViewJobs} startIcon={<WorkIcon />}>
          View Jobs
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

export default EntityCard;