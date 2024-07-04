package com.nextfirsttag.controllers;
import com.nextfirsttag.entities.Connection;
import com.nextfirsttag.services.ConnectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/connections")
@CrossOrigin(origins = "http://localhost:4200")
public class ConnectionController {

    @Autowired
    private ConnectionService connectionService;

    @GetMapping
    public List<Connection> getAllConnections() {
        return connectionService.getAllConnections();
    }

    @GetMapping("/{id}")
    public Connection getConnectionById(@PathVariable Long id) {
        return connectionService.getAllConnections().stream()
                .filter(connection -> connection.getId().equals(id))
                .findFirst()
                .orElse(null);
    }

    @PostMapping
    public Connection saveConnection(@RequestBody Connection connection) {
        return connectionService.saveConnection(connection);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteConnection(@PathVariable Long id) {
        connectionService.deleteConnection(id);
        return ResponseEntity.ok().build();
    }
}
