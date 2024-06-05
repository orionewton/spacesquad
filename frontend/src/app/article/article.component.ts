import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { WikiService } from '../wiki.service';

@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css']
})
export class ArticleComponent implements OnInit {
  content: string;

  constructor(
    private route: ActivatedRoute,
    private wikiService: WikiService
  ) { }

  ngOnInit(): void {
    const filename = this.route.snapshot.paramMap.get('filename');
    this.wikiService.getArticle(filename).subscribe(data => {
      this.content = data;
    });
  }
}
