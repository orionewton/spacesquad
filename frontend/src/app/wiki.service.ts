import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WikiService {
  private apiUrl = 'http://localhost:5000/api/wiki';

  constructor(private http: HttpClient) {}

  getArticle(filename: string): Observable<string> {
    return this.http.get(`${this.apiUrl}/${filename}`, { responseType: 'text' });
  }
}
