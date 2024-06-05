import { Component } from '@angular/core';

@Component({
  selector: 'app-wiki',
  templateUrl: './wiki.component.html',
  styleUrls: ['./wiki.component.css']
})
export class WikiComponent {
  articles = ['article1', 'article2', 'article3']; // Cette liste peut être dynamique

  constructor() { }
}
