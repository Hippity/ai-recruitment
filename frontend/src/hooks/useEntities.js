import { useState, useEffect, useCallback } from 'react';
import { entityService } from '../services/entityService';

export const useEntities = () => {
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchEntities = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await entityService.getEntities();
      setEntities(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching entities:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const createEntity = useCallback(async (entityData) => {
    setError(null);
    try {
      const newEntity = await entityService.createEntity(entityData);
      setEntities(prev => [newEntity, ...prev]);
      return newEntity;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const updateEntity = useCallback(async (id, entityData) => {
    setError(null);
    try {
      const updatedEntity = await entityService.updateEntity(id, entityData);
      setEntities(prev => 
        prev.map(entity => entity.id === id ? updatedEntity : entity)
      );
      return updatedEntity;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const deleteEntity = useCallback(async (id) => {
    setError(null);
    try {
      await entityService.deleteEntity(id);
      setEntities(prev => prev.filter(entity => entity.id !== id));
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  useEffect(() => {
    fetchEntities();
  }, [fetchEntities]);

  return {
    entities,
    loading,
    error,
    fetchEntities,
    createEntity,
    updateEntity,
    deleteEntity,
  };
};