import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Typography,
  Box,
  Paper,
  Chip,
  Divider,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  DragIndicator as DragIcon,
} from '@mui/icons-material';

const CriteriaList = ({ 
  criteria, 
  type, 
  onEdit, 
  onDelete, 
  title,
  emptyMessage = 'No criteria added yet'
}) => {
  const formatScore = (score) => {
    return Number(score).toFixed(score % 1 === 0 ? 0 : 2);
  };

  if (!criteria || criteria.length === 0) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          {emptyMessage}
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ mt: 2 }}>
      <Box sx={{ p: 2, pb: 0 }}>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        {type === 'formal' && (
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Total Max Score: {formatScore(criteria.reduce((sum, c) => sum + (c.max_score || 0), 0))}
          </Typography>
        )}
      </Box>
      
      <List disablePadding>
        {criteria.map((criterion, index) => (
          <React.Fragment key={criterion.id}>
            <ListItem
              sx={{
                alignItems: 'flex-start',
                py: 2,
                '&:hover': {
                  backgroundColor: 'action.hover',
                },
              }}
            >
              <Box sx={{ mr: 1, mt: 1, color: 'action.disabled' }}>
                <DragIcon fontSize="small" />
              </Box>
              
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <Typography variant="subtitle1" component="span">
                      {criterion.area}
                    </Typography>
                    {type === 'formal' && (
                      <Chip
                        label={`${formatScore(criterion.max_score)} pts`}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                    )}
                    <Chip
                      label={`#${criterion.order_index}`}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                }
                secondary={
                  <Box>
                    <Typography variant="body2" color="text.primary" paragraph>
                      {criterion.criteria}
                    </Typography>
                    {criterion.explanation && (
                      <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                        {criterion.explanation}
                      </Typography>
                    )}
                  </Box>
                }
              />
              
              <ListItemSecondaryAction>
                <Box display="flex" flexDirection="column" gap={0.5}>
                  <IconButton
                    edge="end"
                    aria-label="edit"
                    onClick={() => onEdit(criterion)}
                    size="small"
                  >
                    <EditIcon fontSize="small" />
                  </IconButton>
                  <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => onDelete(criterion)}
                    size="small"
                    color="error"
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </Box>
              </ListItemSecondaryAction>
            </ListItem>
            {index < criteria.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>
    </Paper>
  );
};

export default CriteriaList;