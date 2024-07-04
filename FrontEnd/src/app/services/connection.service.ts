// src/app/connection.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Connection } from '../models/connection.model';

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {
  //private apiUrl = 'http://localhost:8081/api/connections';
  private baseUrl = 'http://localhost:8081/api'; // Adjust the base URL as needed
  constructor(private http: HttpClient) {}

  getConnections(): Observable<Connection[]> {
    return this.http.get<Connection[]>(`${this.baseUrl}/connections`);
  }

  addConnection(connection: Connection): Observable<Connection> {
    return this.http.post<Connection>(`${this.baseUrl}/connections`, connection);
  }

  getTagsByConnection(connection: Connection): Observable<string[]> {
    const params = {
      ipAddress: connection.ipAddress,
      name: connection.name,
      gateway: connection.gateway,
      subnet: connection.subnet
    };
    return this.http.get<string[]>(`${this.baseUrl}/readDataTagsFromPlc/${connection.id}`, { params });
  }
}
