package com.nextfirsttag.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.nextfirsttag.entities.Connection;

@Repository
public interface ConnectionRepository extends JpaRepository<Connection, Long> {

  Connection findByName(String connectionName);
}
 