import { Link, useParams } from 'react-router-dom';
import posts from '../data/blogPosts.json';
import { getBlogImage } from '../data/blogImages';
import BlogList from '../components/BlogList';

const formatDate = (value) =>
  new Intl.DateTimeFormat('vi-VN').format(new Date(value));

const ArticleBlock = ({ block, postTitle, index }) => {
  if (block.type === 'heading') {
    return <h2 className="blog-detail__heading">{block.text}</h2>;
  }

  if (block.type === 'image') {
    return (
      <figure className="blog-detail__figure">
        <img
          src={getBlogImage(block.imageKey)}
          alt={block.alt || `${postTitle} - hình ${index + 1}`}
          loading="lazy"
        />
      </figure>
    );
  }

  if (block.type === 'list') {
    return (
      <ul className="blog-detail__list">
        {block.items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    );
  }

  if (block.type === 'quote') {
    return <blockquote className="blog-detail__quote">{block.text}</blockquote>;
  }

  return <p>{block.text}</p>;
};

const BlogDetailPage = () => {
  const { id } = useParams();
  const post = posts.find((item) => String(item.id) === String(id));

  if (!post) {
    return (
      <main className="container blog-detail-not-found">
        <p className="eyebrow">Blog TaloFood</p>
        <h1>Không tìm thấy bài viết</h1>
        <p>Bài viết bạn đang tìm không tồn tại hoặc đường dẫn chưa chính xác.</p>
        <Link className="button button--primary" to="/blog">
          Quay lại Blog
        </Link>
      </main>
    );
  }

  const related = posts.filter((item) => item.id !== post.id).slice(0, 3);

  return (
    <main>
      <article>
        <div className="blog-detail__cover">
          <img src={getBlogImage(post.imageKey)} alt={post.title} />
        </div>

        <div className="container blog-detail__content">
          <Link className="detail-page__back" to="/blog">
            ← Quay lại Blog
          </Link>
          <span className="blog-badge">{post.category}</span>
          <h1>{post.title}</h1>
          <p className="blog-date">Đăng ngày {formatDate(post.publishedAt)}</p>
          <p className="blog-detail__lead">{post.excerpt}</p>

          <div className="blog-detail__article">
            {post.content.map((block, index) => (
              <ArticleBlock
                key={`${block.type}-${index}`}
                block={block}
                postTitle={post.title}
                index={index}
              />
            ))}
          </div>
        </div>
      </article>

      <section className="section blog-related">
        <div className="container">
          <div className="section-heading">
            <h2>Bài viết liên quan</h2>
          </div>
          <BlogList posts={related} />
        </div>
      </section>
    </main>
  );
};

export default BlogDetailPage;
