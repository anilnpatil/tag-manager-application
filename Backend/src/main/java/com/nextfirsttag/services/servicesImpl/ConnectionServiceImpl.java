package com.nextfirsttag.services.servicesImpl;


import com.nextfirsttag.entities.Connection;
import com.nextfirsttag.repositories.ConnectionRepository;
import com.nextfirsttag.services.ConnectionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ConnectionServiceImpl implements ConnectionService{

    @Autowired
    private ConnectionRepository connectionRepository;
    @Override
    public List<Connection> getAllConnections() {
        return connectionRepository.findAll();
    }
    @Override
    public Connection saveConnection(Connection connection) {
        return connectionRepository.save(connection);
    }
    @Override
    public Optional<Connection> getConnectionById(Long id) {
        return connectionRepository.findById(id);
    }
    @Override
    public void deleteConnection(Long id) {
        connectionRepository.deleteById(id);
    }
}
